import os
import requests
import openai

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

api_key  = os.environ['OPENAI_API_KEY']

def download_csv(url: str, file_name: str) -> Any:
    """ This function takes in the url to a csv file and a file name, chosen by the user"""


    if url is None:
        raise ValueError("URL cannot be None")

    if not file_name:
        raise ValueError("File name cannot be empty")

    # Ensure file_name ends with '.pdf'
    if not file_name.lower().endswith('.csv'):
        file_name += '.csv'

    file_path = None

    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            #print("CSV downloaded")
            file_path = f"./{file_name}"
            with open(file_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"File couldn't be downloaded. Status Code: {response.status_code}")

        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading CSV: {e}")
        return file_path

def generate(question:str, csv_path: str | None = None):

    if csv_path is None or csv_path == "./":
      url = "https://github.com/henrii1/DataStructures_implementation/blob/main/csv_data%20-%20Sheet1.csv?raw=True"
      csv_file_name = "transcript"
      csv_path = download_csv(url, csv_file_name)

    loader = CSVLoader(file_path = csv_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter()
    splits = text_splitter.split_documents(data)

    embedding = OpenAIEmbeddings(api_key = api_key)
    vectordb = Chroma.from_documents(
        documents = splits,
        embedding = embedding
    )

    llm = ChatOpenAI(api_key = api_key, temperature = 0, model = "gpt-3.5-turbo")



    response_schema = ResponseSchema(name="response",
                  description="This is a concise response \
                  from the model based on the retrieved context \
                  and the provided question. \
                  Answer 'Yes' or 'No' if the question requires a \
                  Yes/No anwser. else generate a concise response \
                  based on the retrieved context.")
    score_schema = ResponseSchema(name="score",
                  description="This is a numerical score from 0 to 1. \
                  0 means the retrieved context provides no information \
                  that will aid in generating a contextual answer to the \
                  question. 1 means the retrieved context provides all the \
                  information required for generating a contextual answer to\
                  the question. Output should have only one decimal place eg 0.4.")

    output_schemas = [response_schema, score_schema]
    output_parser = StructuredOutputParser.from_response_schemas(output_schemas)
    format_instructions = output_parser.get_format_instructions()


    template = """
    You will be provided with a context and a question. The context is a conversation \
    between a therapist and his/her client. it will begin and end with four hashtags.\
    The question is an inquiry on what was discussed in the conversation. it will begin\
    and end with four backticks. given a context and answer pair,you are to follow the\
    steps below before generating the final answer.

    step 1: Assess the retrieved context and question and output a score from 0 to 1 indicating\
            the extent to which the context provides adequate information for answering the question.\
            the score should have only one decimal place e.g 0.6. 0 means no required information, 1 \
            means all required information is provided.
    step 2: If the score is less than 0.3, politely decline to answer the question, indicating that you\
            do not have enough context to provide an answer. Else proceed to generate a concise answer to \
            the question. make sure the response appropriately answers the question.
    step 3: Only output a valid JSON with the following keys:
            response: the generated answer to the users query. This should be concise.
            score: the numerical value between 0 and 1 that represents the degree to which the context provides\
            enough information for answering the question.

    ####context: {context}####

    ```follow up question: {question}````

    {format_instructions}
    """

    prompt = PromptTemplate(
        template = template,
        input_variables = ["context", "question"],
        partial_variables = {"format_instructions": format_instructions},
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        return_source_documents = False,
        retriever = vectordb.as_retriever(search_type = "mmr", k = 5),
        chain_type_kwargs = {"prompt": prompt}
    )

    result_json = qa_chain.invoke({"query": question})
    output_dict = output_parser.parse(result_json["result"])
    return output_dict["response"], float(output_dict["score"])

