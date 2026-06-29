import streamlit as st
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(
    page_title="AI Customer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Customer Support Assistant")

st.markdown(
    "Analyze customer complaints using Zero-Shot and Few-Shot Prompt Engineering"
)

prompt_type = st.selectbox(
    "Select Prompting Technique",
    ["Zero Shot", "Few Shot"]
)

complaint = st.text_area(
    "Enter Customer Complaint",
    height=150,
    placeholder="Example: My order was supposed to arrive 5 days ago but I still haven't received it."
)

if st.button("Analyze Complaint"):

    if not complaint.strip():
        st.warning("Please enter a complaint.")
        st.stop()

    if prompt_type == "Zero Shot":

        prompt = f"""
        You are an AI Customer Support Assistant.

        Analyze the customer complaint and provide:

        1. Complaint Category
        2. Customer Sentiment
        3. Priority Level
        4. Responsible Department
        5. Professional Response

        Customer Complaint:
        {complaint}

        Format the response clearly.
        """

    else:

        prompt = f"""
        Example 1

        Complaint:
        My package has not arrived.

        Category: Delivery Delay
        Sentiment: Frustrated
        Priority: High
        Department: Logistics

        Response:
        Dear Customer,

        We sincerely apologize for the delay.
        Our logistics team is checking your shipment.

        Regards,
        Support Team

        Example 2

        Complaint:
        I received a damaged phone.

        Category: Damaged Product
        Sentiment: Upset
        Priority: High
        Department: Replacement Team

        Response:
        Dear Customer,

        We apologize for the inconvenience.
        We will arrange a replacement immediately.

        Regards,
        Support Team

        Now analyze:

        Complaint:
        {complaint}
        """

    with st.spinner("Analyzing Complaint..."):

        models = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite"
        ]

        response = None
        used_model = None

        for model_name in models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                used_model = model_name
                break

            except Exception as e:
                st.warning(f"{model_name} unavailable. Trying next model...")

        if response:
            st.success(f"Response generated using: {used_model}")
            st.subheader("Analysis Result")
            st.write(response.text)

        else:
            st.error("All Gemini models are currently unavailable. Please try again later.")