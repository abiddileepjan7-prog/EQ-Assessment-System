"""
Advanced EQ Scoring Engine.
Calculates 0-100 scores for the 5 core EQ dimensions based on transformer NLP
outputs and behavioral keyword indicators.
"""
import re
from .definitions import EQ_DIMENSIONS, POSITIVE_INDICATORS, NEGATIVE_INDICATORS, SCORE_LEVELS


def calculate_eq_scores(responses) -> dict:
    """
    Takes a list of Response model objects (or dicts with similar data)
    and calculates final EQ dimension scores.
    """
    # 1. Initialize all dimension scores to a baseline of 50
    # and track how many questions hit each dimension.
    raw_scores = {dim: 50.0 for dim in EQ_DIMENSIONS}
    weights = {dim: 1.0 for dim in EQ_DIMENSIONS} # base weight
    
    # Track the text so we can look for indicators even if the question wasn't specifically testing that dimension
    all_text_lower = " ".join([r.user_answer for r in responses if r.is_valid]).lower()

    for r in responses:
        if not r.is_valid:
            continue
            
        dim = r.question.eq_dimension
        weights[dim] += 1.5  # Give more weight to dimensions specifically tested
        
        # 2. NLP Metric Adjustments
        # These are heuristics defining what a "good" vs "bad" response looks like per dimension.
        
        # A. Sentiment Impact
        sentiment_upper = r.sentiment_label.upper() if r.sentiment_label else ""
        if sentiment_upper == "POSITIVE":
            # Positive sentiment generally implies better EQ handling (e.g., optimism, resolution)
            raw_scores[dim] += (10.0 * r.sentiment_score)
        else:
            # Negative sentiment isn't inherently bad (e.g. acknowledging sadness = self-awareness),
            # but high intensity negative sentiment without resolution is penalized for
            # dimensions that require composure and constructive engagement.
            if dim in ["self_regulation", "social_skills"]:
                raw_scores[dim] -= (10.0 * r.emotional_intensity)
            elif dim in ["self_awareness", "empathy"]:
                # Acknowledging negative feelings is actually good for awareness/empathy
                raw_scores[dim] += (5.0 * r.emotional_intensity)
                
        # B. Emotion Label Impact
        emo = r.emotion_detected
        if emo in ["joy", "surprise"]:
            if dim in ["motivation", "social_skills"]:
                raw_scores[dim] += 10.0
        elif emo == "anger":
            if dim in ["self_regulation", "social_skills"]:
                raw_scores[dim] -= (15.0 * r.emotional_intensity)
        elif emo == "fear":
            if dim in ["self_regulation", "motivation"]:
                raw_scores[dim] -= (10.0 * r.emotional_intensity)
        elif emo == "sadness":
            if dim == "empathy":
                raw_scores[dim] += 5.0  # Expressing sadness for others is empathetic
            elif dim == "motivation":
                raw_scores[dim] -= (5.0 * r.emotional_intensity)
                
    # 3. Behavioral Indicator Search (Global across all answers)
    for dim in EQ_DIMENSIONS:
        # Check positive indicators
        for ind in POSITIVE_INDICATORS.get(dim, []):
            if re.search(r'\b' + re.escape(ind) + r'\b', all_text_lower):
                raw_scores[dim] += 8.0
                
        # Check negative indicators
        for ind in NEGATIVE_INDICATORS.get(dim, []):
            if re.search(r'\b' + re.escape(ind) + r'\b', all_text_lower):
                raw_scores[dim] -= 12.0

    # 4. Normalization (Clamp all scores between 0 and 100)
    final_scores = {}
    for dim in EQ_DIMENSIONS:
        # We divide by the weight to keep heavily tested dimensions balanced
        normalized = raw_scores[dim] / (weights[dim] / 2.0) if weights[dim] > 1.0 else raw_scores[dim]
        
        # Add a slight random variance (+/- 2) to prevent identical robotic scores 
        # for similar answers, making it feel more organic.
        import random
        variance = random.uniform(-2.0, 2.0)
        normalized += variance
        
        final_scores[dim] = max(0.0, min(100.0, round(normalized, 1)))
        
    # Calculate Overall EQ Score
    overall = sum(final_scores.values()) / len(EQ_DIMENSIONS)
    final_scores["overall_eq_score"] = round(overall, 1)
    
    return final_scores


def get_eq_level(overall_score: float) -> str:
    """
    Maps a 0-100 overall EQ score to a tier key (low / average / high).
    """
    for level_data in SCORE_LEVELS:
        min_val, max_val = level_data["range"]
        if min_val <= overall_score <= max_val:
            return level_data["key"]

    return "average"  # fallback
