import streamlit as st
import asyncio
import edge_tts
import os

st.set_page_config(page_title="Sial AI Stories", page_icon="🎬")

st.title("🎬 Sial AI Stories")
st.subheader("Urdu AI Story Generator")

st.write("Welcome to Sial AI Stories! Enter your prompt below to generate a story.")

prompt = st.text_input("Enter Story Topic (Urdu/English):", "A brave boy in Balochistan")

async def generate_audio(text, output_file="story.mp3"):
    communicate = edge_tts.Communicate(text, "ur-PK-AsadNeural")
    await communicate.save(output_file)

if st.button("Generate Story"):
    if prompt:
        with st.spinner("Generating story and audio..."):
            # Fast Urdu Story Generation
            story_text = (
                f"ایک دفعہ کا ذکر ہے کہ {prompt}۔ وہ بہت بہادر اور عقلمند انسان تھا۔ "
                f"اس نے اپنی محنت، ہمت اور سچائی سے تمام مشکلات کا سامنا کیا "
                f"اور اپنے گاؤں اور علاقے کا نام پوری دنیا میں روشن کر دیا۔"
            )
            
            st.success("Story Generated Successfully!")
            st.write("### 📖 Generated Story:")
            st.write(story_text)
            
            # Fast Audio Generation
            st.info("🎙️ Generating Voice-Over...")
            try:
                if os.path.exists("story.mp3"):
                    os.remove("story.mp3")
                
                asyncio.run(generate_audio(story_text, "story.mp3"))
                
                if os.path.exists("story.mp3"):
                    st.audio("story.mp3", format="audio/mp3")
            except Exception as e:
                st.error(f"Audio Error: {e}")
    else:
        st.warning("Please enter a topic first.")
        
  
