import streamlit as st
import pandas as pd
from dotenv import load_dotenv 
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS 


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = '\n',
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore_openai(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_text(
        text = text_chunks,
        embedding = embeddings
    )
    return vectorstore

def get_vectorstore_instruct(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_text(
        text = text_chunks,
        embedding = embeddings
    )
    return vectorstore




def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDFs", page_icon=":books:")
    st.header("Chat with PDFs :books:")
    st.text_input(label='Ask a question about your documents: ')

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on Process button", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):    
                # get the PDF raw text
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)

                # get the  text chuncks
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)

                # create vector store
                vectorstore = get_vectorstore_instruct(text_chunks)

                # create conversation chain
                conversation = get_conversation_chain(vectorstore)






if __name__ == '__main__':
    main()