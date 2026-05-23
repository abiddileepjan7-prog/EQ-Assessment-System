"""
AI Feedback Engine.
Generates constructive textual feedback, strengths, weaknesses, and actionable recommendations
based on the calculated EQ scores.
"""
from .constants import EQ_DIMENSIONS

# --- Feedback Knowledge Base ---
# In a full LLM integration, these could be prompt instructions. 
# Here, we use a deterministic, high-quality template system.

STRENGTH_FEEDBACK = {
    "self_awareness": "You have a strong understanding of your own emotions and triggers.",
    "self_regulation": "You excel at remaining calm and composed under pressure.",
    "empathy": "You naturally understand and validate the feelings of those around you.",
    "social_skills": "You navigate social interactions and team dynamics with ease.",
    "motivation": "You are highly driven by internal goals and maintain focus during setbacks.",
    "stress_management": "You employ effective coping mechanisms when faced with overwhelming situations.",
    "conflict_resolution": "You are skilled at de-escalating disputes and finding mutually beneficial compromises.",
    "adaptability": "You quickly pivot and adjust your mindset when original plans fall apart.",
    "resilience": "You recover quickly from failures and use them as learning opportunities.",
}

WEAKNESS_FEEDBACK = {
    "self_awareness": "You sometimes struggle to recognize how your mood affects your decision-making.",
    "self_regulation": "You may occasionally act impulsively or let frustration dictate your responses.",
    "empathy": "You might occasionally overlook the underlying emotional drivers of your peers' behaviors.",
    "social_skills": "You sometimes find it challenging to communicate difficult feedback without causing friction.",
    "motivation": "You may lose steam or become discouraged when faced with prolonged obstacles.",
    "stress_management": "High-stakes situations can sometimes cause you to feel overwhelmed or anxious.",
    "conflict_resolution": "You might avoid addressing disputes head-on or struggle to find a middle ground.",
    "adaptability": "Sudden changes to your environment or plans can be highly disruptive for you.",
    "resilience": "You may dwell on past mistakes rather than bouncing back immediately.",
}

RECOMMENDATION_BANK = {
    "self_awareness": "Start a daily reflection journal to track your emotional triggers and responses.",
    "self_regulation": "Practice the '10-second rule'—pause and breathe before responding to an emotionally charged situation.",
    "empathy": "In your next disagreement, focus entirely on actively listening to the other person without preparing your rebuttal.",
    "social_skills": "Practice framing your critiques as 'I feel' statements rather than 'You did' statements.",
    "motivation": "Break your larger goals down into micro-milestones to maintain a sense of achievement during long projects.",
    "stress_management": "Identify your primary physical stress symptom (e.g., tight jaw) and use it as an alarm to take a 5-minute mental break.",
    "conflict_resolution": "When mediating a conflict, try to explicitly restate the other person's core concern before proposing your solution.",
    "adaptability": "Challenge yourself to occasionally change your daily routines to build comfort with unpredictability.",
    "resilience": "After a failure, force yourself to write down three specific, actionable lessons you learned from the experience.",
}

import os
import json
from groq import Groq

def _fallback_generate_feedback(scores: dict) -> dict:
    """
    Fallback: Analyzes the 9 dimension scores to generate static personalized feedback.
    Returns: { "strengths": list, "weaknesses": list, "recommendations": list, "feedback_text": str }
    """
    # Extract only the 9 EQ dimensions (ignoring overall_eq_score)
    dim_scores = {dim: score for dim, score in scores.items() if dim in EQ_DIMENSIONS}
    
    # Sort dimensions by score
    sorted_dims = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Top 3 are strengths, Bottom 2 are weaknesses
    top_3 = [item[0] for item in sorted_dims[:3]]
    bottom_2 = [item[0] for item in sorted_dims[-2:]]
    
    # Generate lists
    strengths = [dim.replace("_", " ").title() for dim in top_3]
    weaknesses = [dim.replace("_", " ").title() for dim in bottom_2]
    
    recommendations = [RECOMMENDATION_BANK[dim] for dim in bottom_2]
    
    # Generate the narrative feedback text
    feedback_text = (
        f"Based on your responses, your emotional intelligence profile is highlighted by your "
        f"capacity for {strengths[0]} and {strengths[1]}. {STRENGTH_FEEDBACK[top_3[0]]} "
        f"However, the assessment indicates that {weaknesses[0]} is an area for potential growth. "
        f"{WEAKNESS_FEEDBACK[bottom_2[0]]} "
        f"By focusing on the provided recommendations, you can significantly elevate your overall EQ."
    )
    
    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "feedback_text": feedback_text
    }


def generate_feedback(scores: dict, scenario_text: str = "", user_answers: dict = None) -> dict:
    """
    Dynamically generates deeply personalized feedback using the GROQ2 API.
    """
    groq_api_key = os.getenv("GROQ2")
    
    if not groq_api_key or not scenario_text or not user_answers:
        return _fallback_generate_feedback(scores)
        
    try:
        client = Groq(api_key=groq_api_key)
        
        # Prepare context for the prompt
        dim_scores = {dim: score for dim, score in scores.items() if dim in EQ_DIMENSIONS}
        sorted_dims = sorted(dim_scores.items(), key=lambda x: x[1], reverse=True)
        top_3 = [item[0] for item in sorted_dims[:3]]
        bottom_2 = [item[0] for item in sorted_dims[-2:]]
        
        strengths_str = ", ".join([d.replace("_", " ").title() for d in top_3])
        weaknesses_str = ", ".join([d.replace("_", " ").title() for d in bottom_2])
        
        user_answers_formatted = "\n".join([f"- {dim.replace('_', ' ').title()}: \"{answer}\"" for dim, answer in user_answers.items()])
        
        prompt = f"""
You are an expert industrial-organizational psychologist writing a personalized Emotional Intelligence (EQ) evaluation.
The user faced this stressful scenario:
"{scenario_text}"

These were their answers to the scenario:
{user_answers_formatted}

Based on our NLP algorithm, their highest scoring strengths are: {strengths_str}.
Their lowest scoring areas for improvement are: {weaknesses_str}.

Write a highly personalized, constructive psychological evaluation.
You MUST respond with ONLY a raw JSON object (no markdown, no backticks).
The JSON object must have exactly these keys:
- "strengths": A list of 3 strings (the user's strengths, formatted beautifully).
- "weaknesses": A list of 2 strings (the user's weaknesses, formatted beautifully).
- "recommendations": A list of 3 highly specific, actionable advice points tailored directly to what they wrote in their answers.
- "feedback_text": A cohesive, empathetic 3-4 sentence paragraph summarizing their profile, directly referencing how they handled the scenario.
"""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        response_content = completion.choices[0].message.content.strip()
        
        if response_content.startswith("```json"):
            response_content = response_content.replace("```json", "", 1)
        if response_content.startswith("```"):
            response_content = response_content.replace("```", "", 1)
        if response_content.endswith("```"):
            response_content = response_content[:-3]
            
        feedback_data = json.loads(response_content.strip())
        
        required_keys = ["strengths", "weaknesses", "recommendations", "feedback_text"]
        if not all(key in feedback_data for key in required_keys):
            raise ValueError("LLM missing required keys.")
            
        return feedback_data
        
    except Exception as e:
        print(f"Groq API Error generating feedback: {e}")
        return _fallback_generate_feedback(scores)
