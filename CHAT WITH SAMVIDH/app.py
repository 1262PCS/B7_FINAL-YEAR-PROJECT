import streamlit as st
from PyPDF2 import PdfReader
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from ctransformers import AutoModelForCausalLM
import os
import requests
import io
import tempfile

# Load model directly
llm = AutoModelForCausalLM.from_pretrained(
    "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
)

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 SAMVIDH')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
    ''')
    st.write('Your Research Guide')

def main():
    st.header("Chat with PDF")
    
    
    embeddings = None
    model = None
    
    # User input: Provide PDF Link
    pdf_link = st.text_input("Enter the link to the PDF file:")
    
    # User input: Query
    query = st.text_area("Ask questions about your PDF file:", height=100)
    
    # Button to process PDF and answer query
    if st.button("Get Answer"):
        pdf_content = download_pdf(pdf_link)
        if pdf_content:
            process_pdf(pdf_content)
            text = extract_text_from_pdf(pdf_content)
            if text:
                chunks = split_text_into_chunks(text)
                embeddings, model = generate_embeddings(chunks)
                answer_query(llm, query, embeddings, model, chunks)
            else:
                st.warning("Failed to extract text from the PDF.")
    
def download_pdf(pdf_link):
    try:
        response = requests.get(pdf_link)
        if response.status_code == 200:
            return response.content
        else:
            st.error("Failed to download the PDF file.")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def process_pdf(pdf_content):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_content)
            tmp_file.seek(0)
            pdf_reader = PdfReader(tmp_file.name)
            num_pages = len(pdf_reader.pages)
        st.success(f"PDF successfully loaded with {num_pages} pages.")
    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {str(e)}")

def extract_text_from_pdf(pdf_content):
    text = ""
    try:
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"An error occurred while extracting text from the PDF: {str(e)}")
        return None

def split_text_into_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,  # Reduce chunk size to 250 characters
        chunk_overlap=100,
        length_function=len
    )
    return text_splitter.split_text(text=text)

def generate_embeddings(chunks):
    sentences = [simple_preprocess(chunk) for chunk in chunks]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    embeddings = []
    for chunk in chunks:
        word_embeddings = [model.wv[word] for word in simple_preprocess(chunk) if word in model.wv]
        if word_embeddings:
            chunk_embedding = np.mean(word_embeddings, axis=0)
        else:
            chunk_embedding = np.zeros(model.vector_size)
        embeddings.append(chunk_embedding)
    return np.array(embeddings), model

def answer_query(llm, query, embeddings, model, chunks):
    if query and embeddings is not None:
        query_embedding = np.mean([model.wv[word] for word in simple_preprocess(query) if word in model.wv], axis=0)
        similar_doc_indices = np.argsort(np.linalg.norm(embeddings - query_embedding, axis=1))[:5]
        similar_docs = [chunks[i] for i in similar_doc_indices]
        prompt = get_prompt(query, similar_docs)
        response = generate_response(llm, prompt)
        # Display previous queries and their answers
        previous_queries = st.session_state.get('previous_queries', [])
        previous_queries.append((query, response))
        st.session_state['previous_queries'] = previous_queries
        for idx, (prev_query, prev_response) in enumerate(previous_queries[::-1]):
            st.text_area(f"Previous Query {len(previous_queries)-idx}:", value=prev_query, height=100, disabled=True)
            st.text_area(f"Previous Answer {len(previous_queries)-idx}:", value=prev_response, height=200, disabled=True)

def generate_response(llm, prompt):
    response = ""
    for word in llm(prompt, stream=True):
        print(word, end="", flush=True)
        response += word
    print()
    return response



def get_prompt(instruction: str, similar_docs: List[str], top_k=3) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Documents:\n"
    for doc in similar_docs[:top_k]:  # Include only top_k similar documents
        prompt += f"- {doc}\n"
    prompt += "\n### Response:\n"
    return prompt



if __name__ == '__main__':
    main()
