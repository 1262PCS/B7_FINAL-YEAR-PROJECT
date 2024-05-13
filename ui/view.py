import pandas as pd
import csv
import networkx as nx
import re
import requests
import os
import PyPDF2
from PyPDF2 import PdfReader

data=pd.read_csv("paper links.csv")
title_data = pd.read_csv("all_papers.csv")

citations_data = pd.read_csv("cora_graph_data.csv")
graph = nx.from_pandas_edgelist(citations_data, source='source', target='target')
citations_title = pd.read_csv("citations.csv")

def paper_data_title(name):
    title = name
    return title
def paper_data_author(name):
    author = data[data['Title'] == name]['Author'].iloc[0]
    return author
def paper_data_Journal(name):
    Journal = data[data['Title'] == name]['Journal'].iloc[0]
    return Journal
def paper_data_citations(name):
    input_node_id = data[data['Title'] == name]['node_id'].iloc[0]
    directed_graph = graph.to_directed()
    
    predecessors = list(directed_graph.predecessors(input_node_id))
    
    cited_node_titles = citations_title.loc[predecessors, 'title'].tolist()
    return cited_node_titles
def paper_pdf_link(name):
    link = data[data['Title'] == name]['Goto PDF'].iloc[0]
    return link
def paper_community(name):
    node_id = data[data['Title']==name]['node_id'].iloc[0]
    community_id = data[data['node_id'] == node_id]['CommunityID'].iloc[0]
    papers_in_community = data[data['CommunityID'] == community_id]['Title'].tolist()
    return papers_in_community
def paper_year(name):
    year = data[data['Title']==name]['Year'].iloc[0]
    return year
def view_abstract(name):
    pdf_link = data[data['Title'] == name]['Goto PDF'].iloc[0]
    try:
        # Disable SSL verification to handle SSL certificate errors
        response = requests.get(pdf_link, stream=True, verify=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the PDF content to a file
            with open('temp_pdf.pdf', 'wb') as file:
                file.write(response.content)

            # Extract first 50 lines from the downloaded PDF
            first_50_lines = extract_first_50_lines('temp_pdf.pdf')

            # Close the file handle after extracting
            try:
                file.close()
            except Exception as e:
                print(f"Error closing file handle: {e}")

            # Delete the temporary PDF file
            try:
                os.remove('temp_pdf.pdf')
            except FileNotFoundError:
                pass

            if first_50_lines:
                return '\n'.join(first_50_lines)
        else:
            print(f"Failed to fetch the PDF from {pdf_link}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the PDF: {e}")


def extract_first_50_lines(pdf_path):
    lines = []
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            lines.extend(text.split('\n')[:20])
            if len(lines) >= 20:
                break  # Break if we have collected 50 lines
    return lines
