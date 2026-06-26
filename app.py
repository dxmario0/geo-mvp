import streamlit as st

st.set_page_config(
    page_title="GEO Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 GEO Analyzer")

st.write("Welcome to GEO MVP 1.0")

question = st.text_input(
    "What would you like to analyze today?",
    placeholder="e.g. ride sharing apps"
)

if st.button("Run GEO Analysis"):

    if question.strip():

        st.success(
            f"Running GEO analysis for:\n\n{question}"
        )

    else:

        st.warning(
            "Please enter a question."
        )
