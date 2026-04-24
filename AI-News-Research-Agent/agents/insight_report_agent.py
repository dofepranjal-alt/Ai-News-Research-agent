from utils.llm import call_grok
from utils.prompts import INSIGHT_REPORT_AGENT_PROMPT

def run_insight_report_agent(analysis: str, summaries: str) -> str:
    """
    Compiles the final report.
    """
    print("[*] Insight/Report Agent compiling final report...")
    user_prompt = f"Analysis:\n{analysis}\n\nSummaries:\n{summaries}\n\nCreate the final report."
    
    response = call_grok(
        system_prompt=INSIGHT_REPORT_AGENT_PROMPT,
        user_prompt=user_prompt,
        temperature=0.5
    )
    
    return response
