import json
from utils.llm import call_grok
from utils.prompts import FILTERING_AGENT_PROMPT
from utils.parser import parse_json_response

def run_filtering_agent(articles_data: str) -> list:
    """
    Filters out irrelevant or low quality articles.
    """
    print("[*] Filtering Agent analyzing articles...")
    user_prompt = f"Articles Data:\n{articles_data}\n\nPlease filter the list and return ONLY a JSON array of the best, most relevant articles."
    
    response = call_grok(
        system_prompt=FILTERING_AGENT_PROMPT + "\nReturn ONLY valid JSON array.",
        user_prompt=user_prompt
    )
    
    return parse_json_response(response)
