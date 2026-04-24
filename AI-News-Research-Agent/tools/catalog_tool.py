import json
import os
from datetime import datetime

CATALOG_FILE = "article_catalog.json"

def save_to_catalog(articles: list, query: str):
    """
    Saves a list of articles to a local JSON catalog.
    """
    catalog = {}
    if os.path.exists(CATALOG_FILE):
        try:
            with open(CATALOG_FILE, "r", encoding="utf-8") as f:
                catalog = json.load(f)
        except json.JSONDecodeError:
            pass
            
    timestamp = datetime.now().isoformat()
    catalog[timestamp] = {
        "query": query,
        "articles": articles
    }
    
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4)
        
    return f"Saved {len(articles)} articles to catalog."
