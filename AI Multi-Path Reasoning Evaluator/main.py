import streamlit as st
from dotenv import load_dotenv
from google import genai
import os

# Load API Key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Page Configuration
st.set_page_config(
    page_title="AI Multi-Path Reasoning Evaluator",
    page_icon="🌳"
)

st.title("🌳 AI Multi-Path Reasoning Evaluator")

st.markdown("""
This application demonstrates Tree of Thoughts / Advanced Chain of Thought Prompting.
The AI generates multiple reasoning paths, evaluates them, and selects the best solution.
""")

problem = st.text_area(
    "Enter a Problem",
    height=150,
    placeholder="Example: A shopkeeper buys 20 notebooks for ₹50 each and sells them for ₹70 each. What is the total profit?"
)

if st.button("Evaluate Reasoning"):

    if not problem.strip():
        st.warning("Please enter a problem.")
        st.stop()

    prompt = f"""
    You are an advanced reasoning evaluator.

    Solve the following problem using Tree of Thoughts reasoning.

    Instructions:

    1. Generate exactly 3 different reasoning paths.
    2. Solve the problem using each reasoning path.
    3. Explain each path clearly.
    4. Compare all reasoning paths.
    5. Select the strongest reasoning path.
    6. Justify why it is the best.
    7. Provide the final answer.

    Problem:
    {problem}
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        st.subheader("Evaluation Result")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
