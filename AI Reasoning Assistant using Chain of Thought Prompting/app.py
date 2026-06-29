import streamlit as st
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(
    page_title="CoT Reasoning Assistant",
    page_icon="🧠"
)

st.title("🧠 Chain of Thought Reasoning Assistant")

problem = st.text_area(
    "Enter a Math or Logic Problem",
    height=150
)

mode = st.radio(
    "Reasoning Mode",
    ["Normal Prompt", "Chain of Thought"]
)

if st.button("Solve Problem"):

    if not problem.strip():
        st.warning("Please enter a problem.")
        st.stop()

    if mode == "Normal Prompt":

        prompt = f"""
        Solve the following problem.

        Problem:
        {problem}
        """

    else:

        prompt = f"""
        You are an expert reasoning assistant.

        Solve the following problem using
        Chain of Thought reasoning.

        Instructions:
        1. Think step-by-step.
        2. Explain each reasoning step.
        3. Show calculations clearly.
        4. Verify the result.
        5. Give the final answer separately.

        Problem:
        {problem}
        """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.subheader("Solution")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")