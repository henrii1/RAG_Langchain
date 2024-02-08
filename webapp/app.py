import os
import requests
import openai
import streamlit as st
from utils import generate

from typing import List, Dict, Any
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file



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

