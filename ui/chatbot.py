from ctransformers import AutoModelForCausalLM
import requests
import re
import os
import pandas as pd
import PyPDF2
from PyPDF2 import PdfReader

llm = AutoModelForCausalLM.from_pretrained(
    "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
)

def get_prompt(instruction: str) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Response:\n"
    return prompt

def view_abstract(pdf_link):
    try:
        # Disable SSL verification to handle SSL certificate errors
        response = requests.get(pdf_link, stream=True, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the PDF content to a file
            with open('temp_pdf.pdf', 'wb') as file:
                file.write(response.content)

            # Extract abstract from the downloaded PDF
            abstract = extract_abstract('temp_pdf.pdf')

            # Delete the temporary PDF file
            try:
                os.remove('temp_pdf.pdf')
            except FileNotFoundError:
                pass

            if abstract:
                print("Abstract:")
                print(abstract)
        else:
            print(f"Failed to fetch the PDF from {pdf_link}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the PDF: {e}")

def extract_abstract(pdf_path):
    abstract_text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            abstract_match = re.search(r'\babstract\b', text, re.IGNORECASE)
            introduction_match = re.search(r'\bintroduction\b', text, re.IGNORECASE)
            if abstract_match:
                if introduction_match:
                    abstract_text += text[abstract_match.end():introduction_match.start()]
                    break
                else:
                    abstract_text += text[abstract_match.end():]
                    break
    return abstract_text.strip()

def chat_interface():
    print("Hi, I am SAMVIDH, I'll be happy to help with your queries! Please choose your requirement:")
    print("1. General Assistance")
    print("2. Display Abstract of a Paper from the link provided")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.")

    while True:
        user_choice = input("Your choice (1/2): ")

        if user_choice.lower() in ["exit", "quit", "bye"]:
            print("Chat ended.")
            break

        if user_choice == "1":
            general_conversation()

        elif user_choice == "2":
            pdf_link = input("Enter the link to the PDF for abstract extraction: ")
            view_abstract(pdf_link)
        else:
            print("Invalid choice. Please enter 1 or 2.")

def general_conversation():
    print("SAMVIDH: Please tell me how can I assist you!")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("SAMVIDH: Moving to main menu!!!!.")
            break

        question = user_input
        prompt = get_prompt(question)
        answer = ""
        print("SAMVIDH: ", end='')

        for word in llm(prompt, stream=True):
            print(word, end="", flush=True)
            answer += word
        print()

# Example usage
# chat_interface()