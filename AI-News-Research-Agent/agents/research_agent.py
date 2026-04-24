import json
from tools.tavily_tool import search_news
from utils.llm import call_grok
from utils.prompts import RESEARCH_AGENT_PROMPT

def run_research_agent(topic: str) -> dict:
    """
    Executes the research phase: gathers articles via Tavily and formats them.
    """
    print(f"[*] Research Agent starting search for: {topic}")
    
    # Get raw search results from Tavily
    raw_results = search_news(topic, max_results=10)
    
    if "error" in raw_results:
        return raw_results
    
    user_prompt = f"Topic: {topic}\n\nRaw Search Results:\n{json.dumps(raw_results.get('results', []), indent=2)}\n\nPlease format these into a clean JSON list of articles with 'url', 'title', 'content_snippet'."
    
    print("[*] Research Agent processing results with Grok...")
    response = call_grok(
        system_prompt=RESEARCH_AGENT_PROMPT + "\nReturn ONLY valid JSON.",
        user_prompt=user_prompt
    )
    
    return {"raw_data": raw_results, "grok_formatted": response}
