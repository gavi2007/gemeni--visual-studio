import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Streamlit UI
st.set_page_config(page_title="Campus Vision Assistant", page_icon="📸")
st.title("📸 Campus Vision & Document Analyzer")
st.write("Upload an image of notes, diagrams, or campus items to analyze using Google Gemini AI.")

# Check for API Key
if not api_key:
    st.error("API Key missing! Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Initialize Google GenAI Client
client = genai.Client(api_key=api_key)

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Prompt option
    prompt_option = st.selectbox(
        "What would you like Gemini to do?",
        [
            "Summarize handwritten/printed study notes",
            "Explain this diagram or chart in detail",
            "Generate a Lost & Found item description",
            "Custom Query"
        ]
    )
    
    custom_prompt = ""
    if prompt_option == "Custom Query":
        custom_prompt = st.text_input("Enter your custom question about the image:")

    if st.button("Analyze Image"):
        # Map selected option to actual prompt
        if prompt_option == "Summarize handwritten/printed study notes":
            user_prompt = "Transcribe and neatly summarize key bullet points from this note."
        elif prompt_option == "Explain this diagram or chart in detail":
            user_prompt = "Explain what this diagram illustrates step-by-step for a student."
        elif prompt_option == "Generate a Lost & Found item description":
            user_prompt = "Describe this object in detail including color, type, and distinct characteristics for a campus Lost & Found post."
        else:
            user_prompt = custom_prompt if custom_prompt else "Describe this image."

        with st.spinner("Analyzing image with Gemini..."):
            try:
                # Call Gemini Multimodal Model
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[image, user_prompt]
                )
                
                st.subheader("Results")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error analyzing image: {e}")
