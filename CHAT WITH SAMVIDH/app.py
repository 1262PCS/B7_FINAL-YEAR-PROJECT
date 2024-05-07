import streamlit as st
from dotenv import load_dotenv
import requests
from PyPDF2 import PdfReader
import io
import tempfile
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from ctransformers import AutoModelForCausalLM
import os

model_path = r"C:\Users\MY PC\Downloads\SAMVIDH FINAL\orca-mini-3b.q4_0.gguf"  # Replace with your model path



# Sidebar contents
with st.sidebar:
    st.title(' SAMVIDH')
    st.markdown('''
        ## About
        Please ask your queries regarding this research paper to SAMVIDH
    ''')
    st.write('Your Research Guide')


def main():
    st.header("Chat with PDF")

    # Initialize embeddings and model (once per session)
    if not os.path.exists(model_path):
        st.error("Model file not found. Please ensure that the model file is located at the specified path.")
        return

    embeddings = None
    model = None

    def initialize_embeddings_and_model():
        global embeddings, model
        #llm = AutoModelForCausalLM.from_pretrained(
        #     "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf")

        llm = AutoModelForCausalLM.from_pretrained(model_path)
        return llm

    llm = initialize_embeddings_and_model()

    # User input: Provide PDF Link
    pdf_link = st.text_input("Enter the link to the PDF file:")
    load_dotenv()

    if st.button("Download and Process"):

        pdf_content = download_pdf(pdf_link)
        if pdf_content:

            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            # st.write(pdf_reader)  # For debugging purposes

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=100, length_function=len
            )
            chunks = text_splitter.split_text(text=text)
            results = generate_word2vec_embeddings(chunks)
            embeddings = results['embeddings']
            model = results['model']

            st.success("PDF processed successfully!")

    # Query input (continuously displayed)
    query = st.text_input("Ask questions about your PDF file:")

    # Flag to keep track of ongoing conversation
    in_conversation = True

    while in_conversation and query:  # Loop for asking and answering questions

        if embeddings is None:  # Check if embeddings are available (handled outside)
            break

        print("QUERY=", query)

        query_embedding = np.mean([model.wv[word] for word in simple_preprocess(query) if word in model.wv], axis=0)
        similar_doc_indices = np.argsort(np.linalg.norm(embeddings - query_embedding, axis=1))[:5]
        similar_docs = [chunks[i] for i in similar_doc_indices]

        prompt = get_prompt(instruction=query, similar_docs=similar_docs)
        response = generate_response(llm, prompt)
        st.write(response)

        # Prompt for next query after each response (within the loop)
        next_query = st.text_input("Next question (or 'exit' to finish):")
        if next_query.lower() == "exit":
            in_conversation = False  # Exit the loop on 'exit'
        else:
            query = next_query  # Update query for the next iteration

    # Outside the loop (if conversation ended or no query entered)
    if embeddings is None:
        st.write("Please upload a PDF to generate embeddings and model.")


def get_prompt(instruction: str, similar_docs: List[str], top_k=3) -> str:

    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Documents:\n"
    for doc in similar_docs[:top_k]:  # Include only top_k similar documents
        prompt += f"- {doc}\n"
    prompt += "\n### Response:\n"
    return prompt

def generate_response(llm, prompt):
    response = ""
    for word in llm(prompt, stream=True):
        print(word, end="", flush=True)
        response += word
        
    return response

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

def generate_word2vec_embeddings(chunks):
    # Train Word2Vec model
    sentences = [simple_preprocess(chunk) for chunk in chunks]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
  
    embeddings = []
    for chunk in chunks:
        # Average the word embeddings in each chunk
        word_embeddings = [model.wv[word] for word in simple_preprocess(chunk) if word in model.wv]
        if word_embeddings:
            chunk_embedding = np.mean(word_embeddings, axis=0)
        else:
            chunk_embedding = np.zeros(model.vector_size)
        embeddings.append(chunk_embedding)
    
    return {'embeddings': np.array(embeddings), 'model': model}

if __name__ == '__main__':
    main()