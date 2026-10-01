import streamlit as st

st.set_page_config(page_title="Sial AI Stories", page_icon="🎬", layout="centered")

st.title("🎬 Sial AI Stories")
st.subheader("Urdu AI Story Generator")

st.write("Welcome to Sial AI Stories! Enter your prompt below to generate a story.")

prompt = st.text_input("Enter Story Topic (Urdu/English):", "A brave boy in Balochistan")

if st.button("Generate Story"):
    st.success(f"Generating story for: {prompt}")
    st.write("---")
    st.write("Once upon a time...")
  
