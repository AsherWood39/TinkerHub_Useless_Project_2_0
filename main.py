
# Main application file for the Intrusive Thoughts Generator
# This Streamlit app takes an image, processes it to find interesting patterns,
# and generates creative stories based on the detected shapes

import streamlit as st
from PIL import Image
import io
import os
from image_cleaning import detect_creases
from groq_interpretation import get_groq_interpretation
from groq_interpretation import image_to_image

st.set_page_config(
    page_title="From the world of Imaginations!", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

with st.container():
    st.title("Intrusive thoughts!")
    st.markdown("Upload a picture of your choice, and let's turn its unique outline into a fictional world with a story.")
    
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=["jpg", "jpeg", "png"],
        help="The clearer the creases, the better the result!",
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

if st.session_state.uploaded_file is not None:
    st.divider()

    st.subheader("Your Original:", anchor=False)
    image = Image.open(st.session_state.uploaded_file)
    max_width = 400
    if image.width > max_width:
        ratio = max_width / float(image.width)
        new_height = int(float(image.height) * ratio)
        image = image.resize((max_width, new_height))
    # Create columns with more space for the center column
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate the Utopia"):
        with st.spinner('Analyzing creases and imagining for you...'):
            # Save the uploaded file to disk
            uploaded_image_path = "uploaded_image.png"
            image.save(uploaded_image_path)
            # Pass the file path to detect_creases
            outline_path = detect_creases(uploaded_image_path)
            st.success("Got the coolest of outlines!")

            st.subheader("Would you like to see the outline?", anchor=False)
            # Center the creased image using columns
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image(outline_path, caption="The outline created from the chaos.", use_container_width=True)

            story = get_groq_interpretation(outline_path)

            st.subheader("Meet with your Creation!")
            generated_image = image_to_image(outline_path, story)
            if os.path.exists(generated_image):
              st.image(generated_image)
            st.markdown("### Time for some Story : ")
            st.write(story)