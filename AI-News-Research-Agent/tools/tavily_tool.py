import os
from tavily import TavilyClient

def search_news(query: str, max_results: int = 5) -> dict:
    """
    Searches for news articles using the Tavily API.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY environment variable not set"}
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            search_depth="advanced",
            include_images=False,
            include_answer=False,
            max_results=max_results,
            topic="news"
        )
        return response
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}
