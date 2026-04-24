import json

def parse_json_response(response_text: str) -> dict:
    """Safely parse JSON from a model response that might contain markdown formatting."""
    try:
        # Strip markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        return json.loads(response_text.strip())
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {"error": "Failed to parse JSON response"}
