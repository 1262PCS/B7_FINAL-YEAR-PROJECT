# -*- coding: utf-8 -*-
"""SAMVIDH FINAL TRIAL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NQNghE4SCtE-YhmdAXnFa9lRpCqtL7c2
"""

!pip install torch-geometric

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch_geometric.nn import GCNConv
from torch_geometric.datasets import Planetoid
from sklearn.metrics import accuracy_score
import re
import tarfile
import gzip

cora_url = 'https://people.cs.umass.edu/~mccallum/data/cora-ie.tar.gz'
cora_tarball_path = 'cora-ie.tar.gz'


!wget {cora_url}

with tarfile.open(cora_tarball_path, 'r:gz') as tar:
    chosen_file = 'cora-ie/tagged_headers.txt.gz'
    gzipped_data = tar.extractfile(chosen_file).read()

decoded_data = gzip.decompress(gzipped_data).decode('utf-8')

pattern = re.compile(r'<NEW_HEADER>(.*?)<NEW_HEADER>', re.DOTALL)
matches = pattern.findall(decoded_data)

data_List = []
for idx, match in enumerate(matches):
    cleaned_match = match.replace('+L+\n\n', '').replace('+L+', '').replace('\n\n', '')

    paper_info = {'paper_id': idx}
    for tag in ['title', 'author', 'abstract', 'affiliation', ]:
        tag_pattern = re.compile(fr'<{tag}>(.*?)<\/{tag}>', re.DOTALL)
        tag_match = tag_pattern.search(cleaned_match)
        if tag_match:
            paper_info[tag] = tag_match.group(1).strip()
        else:
            paper_info[tag] = None
    data_List.append(paper_info)

cora_df = pd.DataFrame(data_List)

dataset = Planetoid(root='.', name='Cora')
data = dataset[0]

class GCN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        return x

model = GCN(in_channels=dataset.num_node_features, hidden_channels=16, out_channels=dataset.num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

def train():
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()

def test():
    model.eval()
    out = model(data.x, data.edge_index)
    pred = out.argmax(dim=1)
    acc = accuracy_score(data.y[data.test_mask].numpy(), pred[data.test_mask].numpy())
    return acc

num_epochs = 200
for epoch in range(1, num_epochs + 1):
    loss = train()
    acc = test()
    print(f'Epoch: {epoch}, Loss: {loss:.4f}, Test Accuracy: {acc:.4f}')

# Final Evaluation
model.eval()
with torch.no_grad():
    # Assuming data contains node features and edge indices
    output = model(data.x, data.edge_index)

# Convert predicted output to categories
predicted_categories = output.argmax(dim=1).cpu().numpy()

# Create a dictionary with enumerated paper IDs starting from 1
data_dict = {'paper_id': list(range(1, len(predicted_categories) + 1)), 'category': predicted_categories}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data_dict)

# Print the DataFrame

merged_df = pd.merge(cora_df, df, on='paper_id')



merged_df.head()

data.merged_df=merged_df

# Dictionary mapping category labels to category names
class_labels_to_names = {
    0: 'Theory',
    1: 'Reinforcement_Learning',
    2: 'Genetic_Algorithms',
    3: 'Neural_Networks',
    4: 'Probabilistic_Methods',
    5: 'Case_Based',
    6: 'Rule_Learning'
}

# Replace category labels with category names in merged_df
merged_df['category'] = merged_df['category'].map(class_labels_to_names)

# Reorder columns in merged_df
merged_df = merged_df.reindex(columns=['paper_id', 'category','title', 'abstract', 'author', 'year', 'affiliation'])

"""# SAMVIDH"""

!pip install ctransformers

from typing import List
from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(
     "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
 )

!pip install pymupdf

!pip install PyPDF2

import requests
import re
import os
import pandas as pd
import PyPDF2
from PyPDF2 import PdfReader


from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained(
    "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
)

# Function to process user query and display relevant papers
def process_and_display_query(query):
    keywords = query.split()

    # Filter the DataFrame based on the keywords and exclude rows with None abstract
    filtered_df = merged_df[(merged_df.apply(lambda row: any(keyword.lower() in str(row) for keyword in keywords), axis=1)) & (merged_df['abstract'].notnull())]

    # Display only the desired columns
    if not filtered_df.empty:
        display(filtered_df[['paper_id', 'category', 'title', 'author', 'abstract']])
    else:
        print("No matching papers found or abstracts are missing.")

def get_prompt(instruction: str) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Response:\n"
    return prompt

def view_abstract(pdf_link):
    response = requests.get(pdf_link, stream=True)

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
from PyPDF2 import PdfReader
import re

def extract_abstract(pdf_path):
    abstract_text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)
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
    print("2. Display Paper Titles as per your requirement")
    print("3. Display Abstract of a Paper from the link provided")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.")

    while True:
        user_choice = input("Your choice (1/2/3): ")

        if user_choice.lower() in ["exit", "quit", "bye"]:
            print("Chat ended.")
            break

        if user_choice == "1":
            general_conversation()
        elif user_choice == "2":
            user_query = input("Enter your query for paper titles: ")
            process_and_display_query(user_query)
        elif user_choice == "3":
            pdf_link = input("Enter the link to the PDF for abstract extraction: ")
            view_abstract(pdf_link)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

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
chat_interface()