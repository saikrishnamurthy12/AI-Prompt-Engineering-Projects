import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load Environment Variables
load_dotenv()

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Page Configuration
st.set_page_config(
    page_title="AI Code Review & Self-Reflection Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Code Review & Self-Reflection Assistant")

st.write(
    "Generate Python code, review it, and automatically improve it using Self-Reflection Prompting."
)

task = st.text_area(
    "Enter Coding Task",
    placeholder="Example: Write a Python function to check whether a number is prime."
)

if st.button("Generate & Improve"):

    if not task.strip():
        st.warning("Please enter a coding task.")
        st.stop()

    try:

        # -----------------------------
        # STEP 1 : Generate Code
        # -----------------------------

        code_prompt = f"""
        You are a Python developer.

        Write a correct Python solution for the following task.

        Requirements:
        - Solve the problem correctly.
        - Keep the solution simple.
        - Do not add docstrings.
        - Do not add test cases.
        - Do not over-optimize.
        - Add only minimal comments if absolutely necessary.
        - Return only Python code.

        Task:
        {task}
        """

        code_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=code_prompt
        )

        generated_code = code_response.text

        # -----------------------------
        # STEP 2 : Review Code
        # -----------------------------

        review_prompt = f"""
        You are a senior software engineer performing a professional code review.

        Review the following Python code.

        Evaluate the code for:

        - Correctness
        - Bugs
        - Edge cases
        - Readability
        - Performance
        - Maintainability
        - Python Best Practices

        List every issue or improvement that should be made.

        If the code is already correct, suggest improvements related to readability,
        documentation, maintainability and coding standards.

        Code:

        {generated_code}
        """

        review_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=review_prompt
        )

        review = review_response.text

        # -----------------------------
        # STEP 3 : Improve Code
        # -----------------------------

        improve_prompt = f"""
        You are a senior Python developer.

        Rewrite the original code using the review.

        Improve:

        - Readability
        - Variable names
        - Code structure
        - Python best practices
        - Documentation
        - Type hints
        - Comments where appropriate

        Fix every issue mentioned in the review.

        Review:

        {review}

        Original Code:

        {generated_code}

        Return only the final improved Python code.
        """

        improved_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=improve_prompt
        )

        improved_code = improved_response.text

        # -----------------------------
        # Display Results
        # -----------------------------

        st.subheader("📝 Step 1 : Initial Code")
        st.code(generated_code, language="python")

        st.subheader("🔍 Step 2 : Self Review")
        st.write(review)

        st.subheader("✨ Step 3 : Improved Code")
        st.code(improved_code, language="python")
        st.subheader("📈 Reflection Summary")

        summary_prompt = f"""
        Summarize the improvements made between the original code and the improved code.

        Keep it short.

        Mention:
        - What changed
        - Why it was changed
        - Benefits of the improvements
        """

        summary = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=summary_prompt
        )

        st.success(summary.text)
    except Exception as e:
        error = str(e)
        if "503" in error:
            st.warning(
                "⚠️ Gemini service is temporarily unavailable.\n\n"
                "This is a server-side issue. Please wait a few moments and try again."
            )

        elif "429" in error:
            st.warning(
                "⚠️ Gemini API quota exceeded.\n\n"
                "Please wait for the quota to reset or use another project/API key."
            )

        else:
            st.error(error)