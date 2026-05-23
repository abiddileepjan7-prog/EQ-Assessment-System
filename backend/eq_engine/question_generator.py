"""
Question Generator — Dynamically creates contextual EQ questions.
"""
import os
import json
import random
from groq import Groq
from .constants import EQ_DIMENSIONS

def generate_questions(scenario_type: str, scenario_text: str = "") -> list[dict]:
    """
    Generates exactly 9 highly tailored questions based on the scenario using Groq LLM.
    Returns: list of dicts {"eq_dimension": str, "question_text": str, "order": int}
    """
    groq_api_key = os.getenv("GROQ")
    
    if not groq_api_key or not scenario_text:
        raise ValueError("GROQ API key or scenario text is missing. Ensure the Django server has restarted to load the .env file.")
        
    try:
        client = Groq(api_key=groq_api_key)
        
        dimensions_list = ", ".join(EQ_DIMENSIONS)
        
        prompt = f"""
You are an expert psychological assessor. Read the following stressful workplace scenario:
"{scenario_text}"

Based on this scenario, generate exactly 9 questions that ask the user how they would handle it.
You MUST generate exactly 1 question for EACH of the following 9 Emotional Intelligence dimensions:
[{dimensions_list}]

Make the questions highly specific to the scenario details.
You MUST respond with ONLY a raw JSON array of objects (no markdown, no backticks).
Each object must have exactly these keys:
- "eq_dimension": The specific EQ dimension (must be from the list).
- "order": Integer from 1 to 9.
- "question_text": The tailored question.
"""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        response_content = completion.choices[0].message.content.strip()
        
        # Clean up markdown
        if response_content.startswith("```json"):
            response_content = response_content.replace("```json", "", 1)
        if response_content.startswith("```"):
            response_content = response_content.replace("```", "", 1)
        if response_content.endswith("```"):
            response_content = response_content[:-3]
            
        questions_data = json.loads(response_content.strip())
        
        if not isinstance(questions_data, list) or len(questions_data) < 5:
            raise ValueError("LLM did not return a valid array of questions.")
            
        return questions_data
        
    except Exception as e:
        print(f"Groq API Error generating questions: {e}")
        raise Exception(f"Failed to generate questions via Groq: {str(e)}")
