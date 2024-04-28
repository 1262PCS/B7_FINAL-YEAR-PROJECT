import csv

def load_papers(filename):
    """Loads paper data from a CSV file into a list of dictionaries.

    Args:
        filename: The path to the CSV file.

    Returns:
        A list of dictionaries, where each dictionary represents a paper with
        keys corresponding to the CSV column headers (e.g., "category", "title").
    """
    papers = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            papers.append(row)
    return papers

def search_papers(keyword, papers):
    """Searches for papers containing the given keyword in category or title.

    Args:
        keyword: The keyword to search for (case-insensitive).
        papers: A list of dictionaries representing papers.

    Returns:
        A list of dictionaries matching the search criteria.
    """
    keyword = keyword.lower()  # Make search case-insensitive
    matching_papers = []
    for paper in papers:
        if 'category' in paper and keyword in paper['category'].lower():
            matching_papers.append(paper)
        elif 'title' in paper and keyword in paper['title'].lower():
            matching_papers.append(paper)
    return matching_papers

# Example usage:
filename = "all_papers.csv"
papers_data = load_papers(filename)
keyword = "machine learning"
matching_papers = search_papers(keyword, papers_data)
for paper in matching_papers:
    print(paper)
