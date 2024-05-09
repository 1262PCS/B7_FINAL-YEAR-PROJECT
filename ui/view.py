import pandas as pd
import csv
import networkx as nx
data=pd.read_csv("updated_dataset.csv")
title_data = pd.read_csv("all_papers.csv")

citations_data = pd.read_csv("cora_graph_data.csv")
graph = nx.from_pandas_edgelist(citations_data, source='source', target='target')
citations_title = pd.read_csv("citations.csv")
title_data_final = title_data.drop_duplicates(subset='Paper Title', keep='first')
title_data_final.to_csv("all_papers_unique.csv", index=False)


def paper_data_title(name):
    node_id = title_data_final[title_data_final['Paper Title'] == name]['Id'].iloc[0]

    # Retrieve the title from data DataFrame based on the node ID
    title = data[data['node_id'] == node_id]['Title'].iloc[0]

    return title
def paper_data_author(name):
    node_id = title_data_final[title_data_final['Paper Title'] == name]['Id'].iloc[0]

    # Retrieve the Author from data DataFrame based on the node ID
    author = data[data['node_id'] == node_id]['Author'].iloc[0]
    return author
def paper_data_publisher(name):
    node_id = title_data_final[title_data_final['Paper Title'] == name]['Id'].iloc[0]

    # Retrieve the Author from data DataFrame based on the node ID
    Publisher = data[data['node_id'] == node_id]['Publisher'].iloc[0]
    return Publisher
def paper_data_citations(name):
    input_node_id = title_data_final[title_data_final['Paper Title'] == name]['Id'].iloc[0]
    
    # Convert graph to a directed graph
    directed_graph = graph.to_directed()
    
    # Find predecessors in the directed graph
    predecessors = list(directed_graph.predecessors(input_node_id))
    
    # Assuming you have a DataFrame (data) containing node titles
    cited_node_titles = citations_title.loc[predecessors, 'title'].tolist()
    return cited_node_titles