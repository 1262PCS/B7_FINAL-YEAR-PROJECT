import pandas as pd
import csv


# Specify the path to your CSV file
file_path = "all_papers.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

def search_papers(keyword):
  """
  This function searches for papers based on a provided keyword in the all_papers_df DataFrame.

  Args:
      keyword: The keyword to search for (lowercase).

  Returns:
      A DataFrame containing matching papers.
  """

  
  keyword = keyword.lower()  # Convert keyword to lowercase for case-insensitive search
  matching_papers = df[df['Paper Title'].str.lower().str.contains(keyword)] 
#   matching_papers = df[df['Paper Title'].str.contains(keyword)]
  return matching_papers

def display_results(matching_papers):
  """
  This function displays the search results with paper titles and other relevant information.

  Args:
      matching_papers: A DataFrame containing matching papers.
  """

  if matching_papers.empty:
    return("No results found.")


#   num_papers = len(matching_papers)
# #   print(f"\nSearch Results for '{keyword}' ({num_papers} papers):\n")
  
  # Access paper titles and potentially other columns you want to display
  paper_titles = matching_papers['Paper Title'].tolist()
  list=[]
  for title in paper_titles:
      el=title
      if el in list:
        continue
      else:
        list.append(el)
  # if len(list)<5:
    # for i in list:
      # print(i)
    
  # else:
  # list=list[:5]
    # for i in list:
      # print(i)
  return list
    

  # print(list) 

# # Example usage
# keyword = input("Enter your search keyword: ")
# matching_papers = search_papers(keyword)
# display_results(matching_papers)
# keyword=input("Enter: ")
# matching_papers=search_papers(keyword)
# paper_data(matching_papers,data)