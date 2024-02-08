import streamlit as st
from utils import generate



def main():
    st.title("RAG POC Chatbot")
    st.write("Ask questions based on the therapy session and get a response")

    texts = st.text_area("Enter your questions here")

    file_uploaded = st.sidebar.file_uploader(
        "Upload a CSV file containing the transcript", key="file_upload"
    )

    if st.sidebar.button("Upload CSV File"):
        if file_uploaded:
           file_content = file_uploaded.read()

    if st.button("Ask Question"):
        with st.spinner(text="Generating"):
            response, score = generate(texts)
            st.markdown(response)
            st.code(score)
       

if __name__ == "__main__":
    main()

