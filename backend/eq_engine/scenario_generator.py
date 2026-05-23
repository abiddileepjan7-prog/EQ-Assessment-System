"""
Scenario Generator — Dynamically creates profession-aware emotional scenarios.
"""
import os
import json
import random
from groq import Groq
import os
import json
from groq import Groq

def generate_scenario(profession: str, age: int) -> dict:
    """
    Generates a personalized scenario dynamically using Groq LLM.
    Returns a dict with scenario_text, scenario_type, profession_group, difficulty.
    """
    groq_api_key = os.getenv("GROQ")
    
    if not groq_api_key:
        raise ValueError("GROQ API key is missing from the environment variables. Please restart your Django backend server so it can load the .env file.")
        
    try:
        client = Groq(api_key=groq_api_key)
        
        prompt = f"""
You are an expert industrial-organizational psychologist designing an emotional intelligence assessment.
Generate a realistic, highly stressful workplace scenario tailored for a {age}-year-old {profession if profession else 'professional'}.
The scenario should be 2-3 sentences long and put the user in a difficult emotional or ethical dilemma.

You MUST respond with ONLY a raw JSON object (no markdown formatting, no backticks, no explanations) containing exactly these 4 keys:
- "scenario_text": The 2-3 sentence stressful scenario.
- "scenario_type": A short category string (e.g., "workplace_conflict", "ethical_dilemma", "unexpected_failure", "high_pressure_decision").
- "profession_group": A general category like "technical", "medical", "management", "creative", or "general".
- "difficulty": "hard" or "medium" based on the psychological complexity.
"""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        response_content = completion.choices[0].message.content.strip()
        
        # Clean up possible markdown backticks if the LLM ignores instructions
        if response_content.startswith("```json"):
            response_content = response_content.replace("```json", "", 1)
        if response_content.startswith("```"):
            response_content = response_content.replace("```", "", 1)
        if response_content.endswith("```"):
            response_content = response_content[:-3]
            
        scenario_data = json.loads(response_content.strip())
        
        # Validate keys
        required_keys = ["scenario_text", "scenario_type", "profession_group", "difficulty"]
        if not all(key in scenario_data for key in required_keys):
            raise ValueError("LLM JSON response missing required keys.")
            
        return scenario_data
        
    except Exception as e:
        print(f"Groq API Error generating scenario: {e}")
        raise Exception(f"Failed to generate scenario via Groq: {str(e)}")
