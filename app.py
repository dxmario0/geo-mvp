import streamlit as st

from pipeline import run_geo_pipeline


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

        with st.spinner("Running GEO pipeline..."):

            result = run_geo_pipeline(question)

        st.success("Prompt Discovery completed!")

        st.write(result)

    else:

        st.warning(
            "Please enter a question."
        )
