import streamlit as st
import os

from dotenv import load_dotenv
from google import genai

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Load API Key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Wikipedia Tool
wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper()
)

# UI
st.set_page_config(
    page_title="Wikipedia Research Agent",
    page_icon="📚"
)

st.title("📚 Wikipedia Research Agent")

st.write(
    "ReAct Prompting - Reasoning + Acting using Wikipedia"
)

query = st.text_input(
    "Ask a Question",
    placeholder="Who invented Python?"
)

if st.button("Search & Answer"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:

        ###############################
        # ACT
        ###############################

        wiki_result = wiki.run(query)

        ###############################
        # REASON
        ###############################

        prompt = f"""
You are an intelligent research assistant.

Question:
{query}

Wikipedia Information:
{wiki_result}

Instructions:

1. Read the Wikipedia information carefully.
2. Analyze the information.
3. Explain the answer clearly.
4. Keep the answer concise.

Provide only the final answer.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        ###############################
        # OUTPUT
        ###############################

        st.subheader("Thought")

        st.info(
            "The system determined that external information "
            "was required before answering."
        )

        st.subheader("Action")

        st.success("Wikipedia Search Completed")

        st.subheader("Observation")

        st.write(wiki_result)

        st.subheader("Final Answer")

        st.write(response.text)

    except Exception as e:

        st.error(e)
