import streamlit as st
import asyncio
import edge_tts
import os
import requests

st.set_page_config(page_title="Sial AI Stories", page_icon="🎬", layout="centered")

st.title("🎬 Sial AI Stories")
st.subheader("Professional Multi-Voice Text-to-Speech & AI Generator")

app_mode = st.sidebar.radio("Select Mode:", ["1. Custom Text-to-Speech (Apna Text)", "2. Free AI Story Generator"])

# Complete 60 Natural Voices (30 Male + 30 Female + Special Styles)
VOICES = {
    # --- SPECIAL & CELEBRITY STYLES ---
    "🕌 Islamic Respectful Voice (Urdu Soft)": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "-5%"},
    "🇵🇰 Imran Khan Style (Deep Male)": {"id": "ur-PK-AsadNeural", "pitch": "-4Hz", "rate": "+0%"},
    "🏏 Babar Azam Style (Calm Male)": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "-5%"},
    "👔 Nawaz Sharif Style (Slow Deep Male)": {"id": "ur-PK-AsadNeural", "pitch": "-6Hz", "rate": "-10%"},
    "⚡ Shahbaz Sharif Style (Fast Male)": {"id": "ur-PK-AsadNeural", "pitch": "-2Hz", "rate": "+15%"},
    "👩‍💼 Maryam Nawaz Style (Confident Female)": {"id": "ur-PK-UzmaNeural", "pitch": "+2Hz", "rate": "+0%"},
    "📜 Shayari & Poet Style (Dramatic Voice)": {"id": "ur-PK-AsadNeural", "pitch": "-4Hz", "rate": "-10%"},

    # --- 30 MALE VOICES ---
    "Male 01 - Urdu Pakistan (Asad)": {"id": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 02 - Arabic Saudi Arabia (Hamed)": {"id": "ar-SA-HamedNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 03 - Arabic UAE (Hamdan)": {"id": "ar-AE-HamdanNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 04 - Arabic Egypt (Shakir)": {"id": "ar-EG-ShakirNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 05 - English US (Guy - TikTok Style)": {"id": "en-US-GuyNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 06 - English US (Andrew Multilingual)": {"id": "en-US-AndrewMultilingualNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 07 - English US (Brian Multilingual)": {"id": "en-US-BrianMultilingualNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 08 - English US (Christopher)": {"id": "en-US-ChristopherNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 09 - English US (Eric)": {"id": "en-US-EricNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 10 - English US (Roger)": {"id": "en-US-RogerNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 11 - English UK (Ryan)": {"id": "en-GB-RyanNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 12 - English UK (Thomas)": {"id": "en-GB-ThomasNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 13 - English IN (Prabhat)": {"id": "en-IN-PrabhatNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 14 - Hindi (Madhur)": {"id": "hi-IN-MadhurNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 15 - Spanish (Alvaro)": {"id": "es-ES-AlvaroNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 16 - French (Henri)": {"id": "fr-FR-HenriNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 17 - German (Conrad)": {"id": "de-DE-ConradNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 18 - Italian (Diego)": {"id": "it-IT-DiegoNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 19 - Turkish (Ahmet)": {"id": "tr-TR-AhmetNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 20 - Russian (Dmitry)": {"id": "ru-RU-DmitryNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 21 - Chinese (Yunxi)": {"id": "zh-CN-YunxiNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 22 - Japanese (Keita)": {"id": "ja-JP-KeitaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 23 - Korean (InJoon)": {"id": "ko-KR-InJoonNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 24 - English Australia (William)": {"id": "en-AU-WilliamNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 25 - English Canada (Liam)": {"id": "en-CA-LiamNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 26 - Portuguese (Antonio)": {"id": "pt-BR-AntonioNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 27 - Persian/Farsi (Farid)": {"id": "fa-IR-FaridNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 28 - Bengali (Bashkar)": {"id": "bn-BD-BashkarNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 29 - Indonesian (Ardi)": {"id": "id-ID-ArdiNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Male 30 - Thai (Niwat)": {"id": "th-TH-NiwatNeural", "pitch": "+0Hz", "rate": "+0%"},

    # --- 30 FEMALE VOICES ---
    "Female 01 - Urdu Pakistan (Uzma)": {"id": "ur-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 02 - Arabic Saudi Arabia (Zariyah)": {"id": "ar-SA-ZariyahNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 03 - Arabic UAE (Fatima)": {"id": "ar-AE-FatimaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 04 - Arabic Egypt (Salma)": {"id": "ar-EG-SalmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 05 - English US (Jenny - TikTok Style)": {"id": "en-US-JennyNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 06 - English US (Ava Multilingual)": {"id": "en-US-AvaMultilingualNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 07 - English US (Emma Multilingual)": {"id": "en-US-EmmaMultilingualNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 08 - English US (Ana Child)": {"id": "en-US-AnaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 09 - English US (Aria)": {"id": "en-US-AriaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 10 - English US (Michelle)": {"id": "en-US-MichelleNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 11 - English UK (Sonia)": {"id": "en-GB-SoniaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 12 - English UK (Libby)": {"id": "en-GB-LibbyNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 13 - English IN (Neerja)": {"id": "en-IN-NeerjaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 14 - Hindi (Swara)": {"id": "hi-IN-SwaraNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 15 - Spanish (Elvira)": {"id": "es-ES-ElviraNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 16 - French (Denise)": {"id": "fr-FR-DeniseNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 17 - German (Katja)": {"id": "de-DE-KatjaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 18 - Italian (Elsa)": {"id": "it-IT-ElsaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 19 - Turkish (Emel)": {"id": "tr-TR-EmelNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 20 - Russian (Svetlana)": {"id": "ru-RU-SvetlanaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 21 - Chinese (Xiaoxiao)": {"id": "zh-CN-XiaoxiaoNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 22 - Japanese (Nanami)": {"id": "ja-JP-NanamiNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 23 - Korean (SunHi)": {"id": "ko-KR-SunHiNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 24 - English Australia (Natasha)": {"id": "en-AU-NatashaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 25 - English Canada (Clara)": {"id": "en-CA-ClaraNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 26 - Portuguese (Francisca)": {"id": "pt-BR-FranciscaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 27 - Persian/Farsi (Dilara)": {"id": "fa-IR-DilaraNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 28 - Bengali (Nabanita)": {"id": "bn-BD-NabanitaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 29 - Indonesian (Gadis)": {"id": "id-ID-GadisNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female 30 - Thai (Premwadee)": {"id": "th-TH-PremwadeeNeural", "pitch": "+0Hz", "rate": "+0%"}
}

# Category/Gender Filter Selection
st.write("---")
gender_filter = st.radio("Filter Voices:", ["All Voices (60+)", "Male Voices (30)", "Female Voices (30)", "Celebrity & Special Styles"], horizontal=True)

if gender_filter == "Male Voices (30)":
    filtered_voices = {k: v for k, v in VOICES.items() if k.startswith("Male")}
elif gender_filter == "Female Voices (30)":
    filtered_voices = {k: v for k, v in VOICES.items() if k.startswith("Female")}
elif gender_filter == "Celebrity & Special Styles":
    filtered_voices = {k: v for k, v in VOICES.items() if not k.startswith("Male") and not k.startswith("Female")}
else:
    filtered_voices = VOICES

selected_voice_name = st.selectbox("Choose Voice:", list(filtered_voices.keys()))
selected_voice_cfg = filtered_voices[selected_voice_name]

# Pitch & Rate Manual Adjustments
col_pitch, col_rate = st.columns(2)
with col_pitch:
    pitch_val = st.slider("Pitch Adjustment (Hz):", min_value=-20, max_value=20, value=0, step=2)
with col_rate:
    rate_val = st.slider("Speed Adjustment (%):", min_value=-30, max_value=30, value=0, step=5)

# Dynamic Pitch & Speed Calculation
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
        "بسم الله الرحمن الرحيم - مرحبا بك! يمكنك اختيار أي صوت لسماع النص."
    )
    
    if st.button("Generate & Speak Audio"):
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

        
        
  
