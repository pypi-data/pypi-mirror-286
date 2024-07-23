"""
SearchUtil: Provides functionality for performing web searches using the Google Custom Search API.
"""

import os
from googleapiclient.discovery import build
from typing import List, Dict

# Load your API key and Custom Search Engine ID from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

def google_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a Google search using the Custom Search API.

    Args:
        query (str): The search query.
        num_results (int): The number of search results to return. Default is 5.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing search results.
    """
    try:
        service = build("customsearch", "v1", developerKey=API_KEY)
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=num_results).execute()
        
        results = []
        for item in res.get('items', []):
            results.append({
                'title': item['title'],
                'link': item['link'],
                'snippet': item['snippet']
            })
        
        return results
    except Exception as e:
        print(f"An error occurred during the search: {str(e)}")
        return []