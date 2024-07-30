import streamlit as st
from ai71 import AI71
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
AI71_API_KEY = os.getenv("AI71_API_KEY")

def generate_response(system_message, user_message):
    response_text = ""
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content
    return response_text

# Streamlit app layout
st.title("AI71 Chat Assistant")

# Input fields
system_message = st.text_area("System Message", value="You are a helpful assistant.")
user_message = st.text_area("User Message", value="Hello!")

if st.button("Generate Response"):
    with st.spinner("Generating response..."):
        response = generate_response(system_message, user_message)
        st.text_area("Response", value=response, height=300)
