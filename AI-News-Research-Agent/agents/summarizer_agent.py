import json
from utils.llm import call_grok
from utils.prompts import SUMMARIZER_AGENT_PROMPT

def run_summarizer_agent(filtered_articles: list) -> str:
    """
    Summarizes the filtered articles.
    """
    print("[*] Summarizer Agent summarizing articles...")
    articles_text = json.dumps(filtered_articles, indent=2)
    user_prompt = f"Filtered Articles:\n{articles_text}\n\nPlease provide concise summaries for each."
    
    response = call_grok(
        system_prompt=SUMMARIZER_AGENT_PROMPT,
        user_prompt=user_prompt
    )
    
    return response
