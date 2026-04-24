import os
from openai import OpenAI

def call_grok(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """
    Calls the Grok (xAI) API using the OpenAI client.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
        
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Recommended current model for Groq
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    
    return response.choices[0].message.content
