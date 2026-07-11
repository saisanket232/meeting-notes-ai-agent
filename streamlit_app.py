import json
import streamlit as st

from agents.meeting_agent import analyze_meeting
from utils import save_json

st.set_page_config(
    page_title="AI Meeting Notes Agent",
    page_icon="📝",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center;'>AI Meeting Notes Agent</h1>",
    unsafe_allow_html=True
)

st.markdown("""
Upload a meeting transcript and automatically generate:

- Meeting Summary
- Key Decisions
- Action Items
- Downloadable JSON Report

Powered by Groq API.
""")

st.divider()

left_spacer, center_col, right_spacer = st.columns([1, 2, 1])

with center_col:
    st.markdown(
        "<h4 style='text-align: center;'>Upload Meeting Transcript</h4>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Meeting Transcript",
        type=["txt"],
        label_visibility="collapsed"
    )

    st.info(
        "Upload a .txt transcript to generate a summary, key decisions, action items, and a downloadable JSON report.",
        icon="ℹ️"
    )

with left_spacer:
    st.empty()

with right_spacer:
    st.empty()

if uploaded_file:

    transcript = uploaded_file.read().decode("utf-8")

    st.subheader("Meeting Transcript")

    st.text_area(
        "Transcript",
        transcript,
        height=200,
        label_visibility="collapsed"
    )

    if st.button("Analyze Meeting"):

        with st.spinner("Analyzing..."):

            response = analyze_meeting(transcript)

            data = json.loads(response)

            save_json(
                data,
                "output/meeting_summary.json"
            )

        st.success("Analysis Complete!")

        st.subheader("Meeting Summary")

        st.write(data["Meeting Summary"])

        st.subheader("Key Decisions")

        st.write(data["Key Decisions"])

        st.subheader("Action Items")

        st.table(data["Action Items"])

        with open(
            "output/meeting_summary.json",
            "rb"
        ) as file:

            st.download_button(
                "Download JSON",
                file,
                file_name="meeting_summary.json"
            )