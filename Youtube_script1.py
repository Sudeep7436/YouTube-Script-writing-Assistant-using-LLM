import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as palm

# Load environment variables
load_dotenv()

# Set up Google Gemini API key securely
palm.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
model = palm.GenerativeModel('gemini-1.5-flash')
# Function to generate a YouTube script using Google Gemini
def generate_script(style, format, audience, topic):
    prompt = f"""
    You are a creative YouTube script writer. Write a {format} YouTube script tailored for {audience}. 
    The tone should be {style}. The video topic is: {topic}.
    Provide a catchy intro, engaging body, and a memorable outro.
    """
    try:
        response = model.generate_content(prompt)
        return response.text  # Retrieve the final response content
    except Exception as e:
        return f"Error: {e}"

# Streamlit App UI
st.title("YouTube Script Writing Assistant (Google Gemini)")

st.sidebar.header("Input Details")
style = st.sidebar.selectbox("Select Style", ["Casual", "Professional", "Humorous", "Inspirational"])
format = st.sidebar.selectbox("Select Format", ["Tutorial", "Storytelling", "Explainer", "Interview"])
audience = st.sidebar.selectbox("Select Audience", ["Beginners", "Professionals", "Teens", "General Audience"])
topic = st.sidebar.text_input("Enter Video Topic", "How to Learn Python Fast")

if st.sidebar.button("Generate Script"):
    with st.spinner("Generating your script..."):
        try:
            script = generate_script(style, format, audience, topic)
            if "Error" in script:
                st.error(script)
            else:
                st.success("Script Generated!")
                st.write(script)
                st.download_button("Download Script", script, file_name="youtube_script.txt")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
