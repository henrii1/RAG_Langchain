import os
import streamlit as st

from utils import download_csv, load_csv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # Read local .env file
api_key = os.environ['OPENAI_API_KEY']


def generate_response(question: str, csv_path: str) -> tuple:
    """Generates response based on question and transcript."""
    loader = CSVLoader(file_path=csv_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter()
    splits = text_splitter.split_documents(data)

    embedding = OpenAIEmbeddings(api_key=api_key)
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding
    )

    llm = ChatOpenAI(api_key=api_key, temperature=0, model="gpt-3.5-turbo")

    response_schema = ResponseSchema(name="response",
                                     description="This is a concise response...")
    score_schema = ResponseSchema(name="score",
                                  description="This is a numerical score from 0 to 1...")
    output_schemas = [response_schema, score_schema]
    output_parser = StructuredOutputParser.from_response_schemas(output_schemas)
    format_instructions = output_parser.get_format_instructions()

    template = """
    You will be provided with a context and a question. The context is a conversation...
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"],
        partial_variables={"format_instructions": format_instructions},
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        return_source_documents=False,
        retriever=vectordb.as_retriever(search_type="mmr", k=5),
        chain_type_kwargs={"prompt": prompt}
    )

    result_json = qa_chain.invoke({"query": question})
    output_dict = output_parser.parse(result_json["result"])
    return output_dict["response"], float(output_dict["score"])

def main():
    st.title("RAG POC Chatbot")
    st.write("Ask questions based on the therapy session and get a response")

    texts = st.text_area("Enter your questions here")

    file_uploaded = st.sidebar.file_uploader(
        "Upload a CSV file containing the transcript", key="file_upload"
    )

    if st.sidebar.button("Upload CSV File"):
        file_path = load_csv(file_uploaded)

    if st.button("Ask Question"):
        if file_uploaded:
            with st.spinner(text="Generating"):
                response, score = generate_response(texts, file_path)
                st.markdown(response)
                st.code(score)
        else:
            st.warning("Please upload a CSV file first.")

if __name__ == "__main__":
    main()
