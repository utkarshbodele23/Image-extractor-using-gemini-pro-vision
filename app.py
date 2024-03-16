from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# function to load Gemini pro vision
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded") 


# streamlit app

st.set_page_config(page_title="Image Extractor")


st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Build_with_Gemini_dk_16_9_1.width-1200.format-webp.webp", 
         width=700)
st.header("Gemini Pro Vision")
st.header("Image Extractor")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image="" 

# to show the uploaded file
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# submit button
submit = st.button("Get Response")

# input prompt
input_prompt = """
You are an expert in understanding images, especially text in the images like name, phone number.
We will upload an image having lots of text information in it and you will have to answer the questions
based on the uploaded image.
"""

# if submit buttion is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is")
    st.write(response)