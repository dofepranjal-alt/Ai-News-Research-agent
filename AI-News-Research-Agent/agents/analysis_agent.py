from utils.llm import call_grok
from utils.prompts import ANALYSIS_AGENT_PROMPT

def run_analysis_agent(summaries: str) -> str:
    """
    Analyzes the summaries for trends and narratives.
    """
    print("[*] Analysis Agent analyzing summaries...")
    user_prompt = f"Summaries:\n{summaries}\n\nPlease provide an analysis."
    
    response = call_grok(
        system_prompt=ANALYSIS_AGENT_PROMPT,
        user_prompt=user_prompt
    )
    
    return response
