# tryon/utils.py
from serpapi import GoogleSearch

def search_dresses(query, api_key,gender=None):
    """
    Search for dresses based on the style query and retrieve image and link details.
    """
    if gender:
        search_query = f"{gender} {query} full-body dress"  # Filter for gender and full-body
    else:
        search_query = f"{query} full-body dress"# Append "dress" to style for better results

    # Parameters for SerpAPI Google Shopping search
    params = {
        "engine": "google_shopping",
        "q": search_query,
        "api_key": api_key,
        "num": 10,
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en"
    }

    # Initialize the Google Search and fetch results
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract dress details
    dresses = []
    for item in results.get("shopping_results", []):
        dress = {
            "title": item.get("title", "N/A"),
            "price": item.get("price", "N/A"),
            "link": item.get("link", "N/A"),
            "gender":item.get("gender", "male"),
            "thumbnail": item.get("thumbnail", "N/A"),
        }
        dresses.append(dress)

    return dresses
