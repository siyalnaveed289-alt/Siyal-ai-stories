import streamlit as st
import asyncio
import edge_tts
import os

st.set_page_config(page_title="Sial AI Stories", page_icon="🎬")

st.title("🎬 Sial AI Stories")
st.subheader("Urdu AI Story Generator")

st.write("Welcome to Sial AI Stories! Select your character voice and generate a story.")

# Input fields
prompt = st.text_input("Enter Story Topic (Urdu/English):", "ڈاکو عظیم سولنگی")

col1, col2 = st.columns(2)
with col1:
    voice_option = st.selectbox(
        "Select Character Voice:", 
        [
            "Male (Asad)", 
            "Female (Uzma)", 
            "Child / Bacha", 
            "Old Man / Buzurg", 
            "Old Woman / Buri Aurat"
        ]
    )
with col2:
    category = st.selectbox(
        "Story Category:", 
        ["Moral / Sabaq Amoz", "Action / Adventure", "Funny / Mazahiya", "Mystery / Raaz"]
    )

# Voice Configuration Settings
VOICE_CONFIG = {
    "Male (Asad)": {"voice": "ur-PK-AsadNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Female (Uzma)": {"voice": "ur-PK-UzmaNeural", "pitch": "+0Hz", "rate": "+0%"},
    "Child / Bacha": {"voice": "ur-PK-UzmaNeural", "pitch": "+12Hz", "rate": "+10%"},
    "Old Man / Buzurg": {"voice": "ur-PK-AsadNeural", "pitch": "-10Hz", "rate": "-15%"},
    "Old Woman / Buri Aurat": {"voice": "ur-PK-UzmaNeural", "pitch": "-8Hz", "rate": "-12%"},
}

async def generate_audio(text, voice_cfg, output_file="story.mp3"):
    communicate = edge_tts.Communicate(
        text, 
        voice_cfg["voice"], 
        pitch=voice_cfg["pitch"], 
        rate=voice_cfg["rate"]
    )
    await communicate.save(output_file)

def get_story_content(topic, cat):
    if cat == "Moral / Sabaq Amoz":
        return f"ایک زمانے کا ذکر ہے کہ {topic} کے بارے میں سب بات کرتے تھے۔ اس نے اپنی زندگی کے ایک مشکل موڑ پر سچائی اور ایمانداری کا راستے چنا۔ لوگ اسے اس کی عقلمندی اور ہمدردی کی وجہ سے ہمیشہ یاد رکھتے ہیں۔"
    elif cat == "Action / Adventure":
        return f"سنسنی خیز داستان! {topic} نے جب اپنے علاقے کی حفاظت کی ذمہ داری لی تو سب حیران رہ گئے۔ تاریک راتوں اور مشکل راستوں پر اس نے اپنی بہادری سے دشمنوں کے منصوبے خاک میں ملا دیے۔"
    elif cat == "Funny / Mazahiya":
        return f"ایک مزاحیہ کہانی! {topic} جب بھی کوئی نیا کام شروع کرتا، کوئی نہ کوئی عجیب غریب واقعہ پیش آ جاتا۔ پورے گاؤں کے لوگ اس کی معصومانہ حماقتوں پر ہنس ہنس کر لوٹ پوٹ ہو جاتے۔"
    else:
        return f"ایک پراسرار کہانی! {topic} کے گرد ایک عجیب راز چھپا ہوا تھا۔ پرانے قلعے کی خاموشی میں جب بھی اس کا نام لیا جاتا، تو ایک پراسرار ہوا چلنے لگتی جس کا جواب کسی کے پاس نہ تھا۔"

if st.button("Generate Story"):
    if prompt:
        with st.spinner("Generating story..."):
            story_text = get_story_content(prompt, category)
            
            st.success("Story Generated Successfully!")
            st.write("### 📖 Generated Story:")
            st.write(story_text)
            
            st.info(f"🎙️ Generating Character Voice ({voice_option})...")
            try:
                if os.path.exists("story.mp3"):
                    os.remove("story.mp3")
                
                cfg = VOICE_CONFIG[voice_option]
                asyncio.run(generate_audio(story_text, cfg, "story.mp3"))
                
                if os.path.exists("story.mp3"):
                    st.audio("story.mp3", format="audio/mp3")
            except Exception as e:
                st.error(f"Audio Error: {e}")
    else:
        st.warning("Please enter a topic first.")
        
        
  
