import pandas as pd
import csv
import networkx as nx

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
def paper_data_publisher(name):
    Publisher = data[data['Title'] == name]['Publisher'].iloc[0]
    return Publisher
def paper_data_citations(name):
    input_node_id = data[data['Title'] == name]['node_id'].iloc[0]
    # Convert graph to a directed graph
    directed_graph = graph.to_directed()
    
    # Find predecessors in the directed graph
    predecessors = list(directed_graph.predecessors(input_node_id))
    
    # Assuming you have a DataFrame (data) containing node titles
    cited_node_titles = citations_title.loc[predecessors, 'title'].tolist()
    return cited_node_titles
def paper_pdf_link(name):
    link = data[data['Title'] == name]['Goto PDF'].iloc[0]
    return link


