import streamlit as st
import os
import requests

# Set your Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define the model to use
MODEL_ID = "llama-3.3-70b-versatile"

def explain_term(term):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are an expert in engineering and explain technical terms clearly."},
            {"role": "user", "content": f"Explain the engineering term: {term}"}
        ],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="Engineering Term Explainer", layout="centered")
st.title("🔧 Engineering Term Explainer")

term = st.text_input("Enter an engineering term:")

if st.button("Explain"):
    if not GROQ_API_KEY:
        st.error("API key not set. Please set your GROQ_API_KEY as an environment variable or in secrets.")
    elif term.strip() == "":
        st.warning("Please enter a term.")
    else:
        with st.spinner("Explaining..."):
            explanation = explain_term(term)
        st.success("Explanation:")
        st.markdown(explanation)
