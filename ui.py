
import streamlit as st
from PIL import Image
import io
import os
from image_cleaning import detect_creases
from groq_interpretation import get_groq_interpretation
from main import image_to_image

st.set_page_config(
    page_title="From Crumpled Paper to Character!", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

with st.container():
    st.title("From Trash to Wonder!")
    st.markdown("Upload a picture of a creased paper, and let's turn its unique outline into a fictional character with a story.")
    
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

    uploaded_file = st.file_uploader(
        "Choose an image of creased paper...", 
        type=["jpg", "jpeg", "png"],
        help="The clearer the creases, the better the result!",
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

if st.session_state.uploaded_file is not None:
    st.divider()

    st.subheader("Your Original :")
    image = Image.open(st.session_state.uploaded_file)
    max_width = 400
    if image.width > max_width:
        ratio = max_width / float(image.width)
        new_height = int(float(image.height) * ratio)
        image = image.resize((max_width, new_height))
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image(image, caption="Uploaded Image", use_container_width=False)
    
    if st.button("Generate Character"):
        with st.spinner('Analyzing creases and imagining a new character...'):
            outline_path = detect_creases(uploaded_file)
            st.success("Character generated successfully!")

            st.subheader("Your Character's Outline")
            st.image(outline_path, caption="The outline created from your creases.")

            story = get_groq_interpretation(outline_path)

            st.subheader("Meet our new friend!")
            generated_image = image_to_image(outline_path, story)
            if os.path.exists(generated_image):
                st.image("generated_character.png", caption="A valiant knight born from a crease!")
            st.markdown("### The Story")
            st.write(story)

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/api/hello', methods=['GET'])
# def hello():
#     return jsonify({'message': 'Hello from Python!'})

# if __name__ == '__main__':
#     app.run(port=5000)