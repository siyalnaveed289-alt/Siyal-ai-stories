import streamlit as st
import asyncio
import edge_tts
import os
import requests

st.set_page_config(page_title="Sial AI Stories", page_icon="🎬", layout="wide")

st.title("🎬 Sial AI Stories")
st.subheader("Multi-Voice Text-to-Speech & AI Story Generator")

app_mode = st.sidebar.radio("Select Mode:", ["1. Custom Text-to-Speech (Apna Text)", "2. Free AI Story Generator"])

# 20 MALE & 20 FEMALE DEDICATED URDU VOICE CHARACTERS + REGIONAL & ARABIC
VOICES = {
    # ==================== 20 MALE URDU CHARACTERS ====================
    "👨‍💼 Male Urdu 01 - Asad (Standard News/Formal)": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "+0%"},
    "👨‍🏫 Male Urdu 02 - Salman (Soft & Polite)": {"id": "ur-IN-SalmanNeural", "pitch": "+0Hz", "rate": "+0%"},
    "🎙️ Male Urdu 03 - Deep Storyteller (Bhari Aawaz)": {"id": "ur-PK-AsadNeural", "pitch": "-6Hz", "rate": "-5%"},
    "⚡ Male Urdu 04 - Energetic Presenter (Fast & Crisp)": {"id": "ur-PK-AsadNeural", "pitch": "+2Hz", "rate": "+15%"},
    "📻 Male Urdu 05 - Radio RJ Style (Smooth & Warm)": {"id": "ur-IN-SalmanNeural", "pitch": "-2Hz", "rate": "+0%"},
    "👴 Male Urdu 06 - Elderly Grandfather (Buzurg)": {"id": "ur-PK-AsadNeural", "pitch": "-8Hz", "rate": "-15%"},
    "👦 Male Urdu 07 - Young Boy Character": {"id": "ur-PK-AsadNeural", "pitch": "+8Hz", "rate": "+5%"},
    "📜 Male Urdu 08 - Shayari & Poetry Master": {"id": "ur-PK-AsadNeural", "pitch": "-4Hz", "rate": "-10%"},
    "🕌 Male Urdu 09 - Islamic Scholar / Molvi Style": {"id": "ur-PK-AsadNeural", "pitch": "-2Hz", "rate": "-8%"},
    "🇵🇰 Male Urdu 10 - Leader / Politician Style": {"id": "ur-PK-AsadNeural", "pitch": "-5Hz", "rate": "+0%"},
    "💼 Male Urdu 11 - Corporate Businessman": {"id": "ur-IN-SalmanNeural", "pitch": "+0Hz", "rate": "+5%"},
    "🎓 Male Urdu 12 - Teacher / Professor": {"id": "ur-PK-AsadNeural", "pitch": "-2Hz", "rate": "-5%"},
    "😱 Male Urdu 13 - Horror Story Voice (Ghabrahat / Suspense)": {"id": "ur-PK-AsadNeural", "pitch": "-10Hz", "rate": "-15%"},
    "📖 Male Urdu 14 - Historical Narrator (Tareekhi Dastan)": {"id": "ur-PK-AsadNeural", "pitch": "-6Hz", "rate": "-10%"},
    "🏏 Male Urdu 15 - Sports commentator (Joshila)": {"id": "ur-PK-AsadNeural", "pitch": "+4Hz", "rate": "+20%"},
    "🎥 Male Urdu 16 - Movie Trailer Deep Voice": {"id": "ur-PK-AsadNeural", "pitch": "-12Hz", "rate": "-8%"},
    "☕ Male Urdu 17 - Friendly Casual Conversation": {"id": "ur-IN-SalmanNeural", "pitch": "+2Hz", "rate": "+0%"},
    "📢 Male Urdu 18 - Motivational Speaker": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "+10%"},
    "🧘 Male Urdu 19 - Calm & Meditation Guide": {"id": "ur-IN-SalmanNeural", "pitch": "-4Hz", "rate": "-15%"},
    "💡 Male Urdu 20 - Tech & Science Reviewer": {"id": "ur-PK-AsadNeural", "pitch": "+2Hz", "rate": "+5%"},

    # ==================== 20 FEMALE URDU CHARACTERS ====================
    "👩‍💼 Female Urdu 01 - Uzma (Standard News/Formal)": {"id": "ur-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "👩‍🏫 Female Urdu 02 - Gul (Soft & Melodious)": {"id": "ur-IN-GulNeural", "pitch": "+0Hz", "rate": "+0%"},
    "📖 Female Urdu 03 - Storyteller / Dastangoi": {"id": "ur-PK-UzmaNeural", "pitch": "-2Hz", "rate": "-8%"},
    "📻 Female Urdu 04 - Radio RJ / Show Host": {"id": "ur-IN-GulNeural", "pitch": "+2Hz", "rate": "+5%"},
    "👧 Female Urdu 05 - Young Girl Character": {"id": "ur-PK-UzmaNeural", "pitch": "+8Hz", "rate": "+10%"},
    "👵 Female Urdu 06 - Loving Grandmother (Dadi / Nani)": {"id": "ur-PK-UzmaNeural", "pitch": "-6Hz", "rate": "-15%"},
    "📜 Female Urdu 07 - Poetry & Ghazal Reciter": {"id": "ur-IN-GulNeural", "pitch": "-2Hz", "rate": "-10%"},
    "👩‍⚕️ Female Urdu 08 - Professional / Doctor Style": {"id": "ur-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "🎙️️ Female Urdu 09 - Commercial & Ad Voice": {"id": "ur-IN-GulNeural", "pitch": "+4Hz", "rate": "+10%"},
    "🕌 Female Urdu 10 - Respectful Religious Teacher": {"id": "ur-PK-UzmaNeural", "pitch": "-2Hz", "rate": "-8%"},
    "🌸 Female Urdu 11 - Gentle Bedtime Story Narrator": {"id": "ur-IN-GulNeural", "pitch": "-4Hz", "rate": "-12%"},
    "🎓 Female Urdu 12 - School Teacher / Instructor": {"id": "ur-PK-UzmaNeural", "pitch": "+2Hz", "rate": "-2%"},
    "⚡ Female Urdu 13 - Fast News Anchor": {"id": "ur-PK-UzmaNeural", "pitch": "+2Hz", "rate": "+15%"},
    "🎭 Female Urdu 14 - Drama Character (Emotional)": {"id": "ur-IN-GulNeural", "pitch": "-4Hz", "rate": "-5%"},
    "💡 Female Urdu 15 - Tech & Educational Explainer": {"id": "ur-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+5%"},
    "🌟 Female Urdu 16 - Confident & Bold Character": {"id": "ur-PK-UzmaNeural", "pitch": "-2Hz", "rate": "+5%"},
    "🎨 Female Urdu 17 - Creative & Expressive Voice": {"id": "ur-IN-GulNeural", "pitch": "+4Hz", "rate": "+0%"},
    "🍃 Female Urdu 18 - Soft Whispering / Relaxing": {"id": "ur-IN-GulNeural", "pitch": "-6Hz", "rate": "-20%"},
    "🌍 Female Urdu 19 - Documentary Narrator": {"id": "ur-PK-UzmaNeural", "pitch": "-4Hz", "rate": "-8%"},
    "🛍️ Female Urdu 20 - Shopping & Lifestyle Host": {"id": "ur-IN-GulNeural", "pitch": "+6Hz", "rate": "+12%"},

    # ==================== OTHER LANGUAGES & SPECIALS ====================
    "Male - Sindhi Pakistan (Nabeel)": {"id": "sd-PK-NabeelNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female - Sindhi Pakistan (Uzma)": {"id": "sd-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male - Saraiki / Shahpuri (Asad)": {"id": "pnb-PK-AsadNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female - Saraiki / Shahpuri (Uzma)": {"id": "pnb-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male - Arabic Saudi Arabia (Hamed - Quran Best)": {"id": "ar-SA-HamedNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female - Arabic Saudi Arabia (Zariyah)": {"id": "ar-SA-ZariyahNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male - English US (Guy)": {"id": "en-US-GuyNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female - English US (Jenny)": {"id": "en-US-JennyNeural", "pitch": "+0Hz", "rate": "+0%"}
}

# Gender & Category Filter Options
st.write("---")
category_filter = st.radio(
    "Filter Voices Category:", 
    ["All Voices", "Urdu Male Voices (20)", "Urdu Female Voices (20)", "Sindhi & Saraiki", "Arabic / Quran"], 
    horizontal=True
)

if category_filter == "Urdu Male Voices (20)":
    filtered_voices = {k: v for k, v in VOICES.items() if "Male Urdu" in k}
elif category_filter == "Urdu Female Voices (20)":
    filtered_voices = {k: v for k, v in VOICES.items() if "Female Urdu" in k}
elif category_filter == "Sindhi & Saraiki":
    filtered_voices = {k: v for k, v in VOICES.items() if "Sindhi" in k or "Saraiki" in k}
elif category_filter == "Arabic / Quran":
    filtered_voices = {k: v for k, v in VOICES.items() if "Arabic" in k}
else:
    filtered_voices = VOICES

selected_voice_name = st.selectbox("Choose Voice Character:", list(filtered_voices.keys()))
selected_voice_cfg = filtered_voices[selected_voice_name]

# Pitch & Rate Manual Sliders
col_pitch, col_rate = st.columns(2)
with col_pitch:
    pitch_val = st.slider("Fine Pitch Adjustment (Hz):", min_value=-20, max_value=20, value=0, step=2)
with col_rate:
    rate_val = st.slider("Fine Speed Adjustment (%):", min_value=-30, max_value=30, value=0, step=5)

# Calculate final pitch and rate
base_pitch = int(selected_voice_cfg["pitch"].replace("Hz", ""))
base_rate = int(selected_voice_cfg["rate"].replace("%", ""))

final_pitch_num = base_pitch + pitch_val
final_rate_num = base_rate + rate_val

final_pitch = f"{'+' if final_pitch_num >= 0 else ''}{final_pitch_num}Hz"
final_rate = f"{'+' if final_rate_num >= 0 else ''}{final_rate_num}%"

async def generate_audio(text, voice_id, pitch, rate, output_file="story.mp3"):
    # Arabic script detection for slow and clear recitation
    is_arabic_script = any('\u0600' <= char <= '\u06FF' for char in text)
    if is_arabic_script and "ar-" in voice_id:
        rate = "-20%"
        pitch = "+0Hz"
        
    communicate = edge_tts.Communicate(text, voice_id, pitch=pitch, rate=rate)
    await communicate.save(output_file)

# ---------------- MODE 1: CUSTOM TEXT TO SPEECH ----------------
if app_mode == "1. Custom Text-to-Speech (Apna Text)":
    st.write("### 🎙️ Direct Text to Speech")
    user_text = st.text_area(
        "Yahan apna text likhein:", 
        "خوش آمدید! سیال اے آئی اسٹوریز میں اپنا متن درج کریں اور بہترین آواز حاصل کریں۔"
    )
    
    if st.button("Generate & Speak Audio 🎙️"):
        if user_text:
            with st.spinner("Generating High Quality Urdu Audio..."):
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
                                file_name="sial_ai_urdu_voice.mp3",
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
        if prompt:
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
