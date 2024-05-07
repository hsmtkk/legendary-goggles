import streamlit as st
import utils

st.title("Let's do some analysis on your CSV")
st.header("Please upload your CSV file here")

data = st.file_uploader("Upload your CSV file", type="csv")

query = st.text_area("Enter your query")
button = st.button("Generate a response")

if button:
    answer = utils.query_agent(data, query)
    st.write(answer)
