"""
HuggingFace Inference API Pipeline for Emotion and Sentiment Analysis.

Uses the free HuggingFace Inference API to run the exact same transformer models
without requiring a local PyTorch installation — making it compatible with free-tier hosting.
"""
import os
import re
<<<<<<< HEAD:backend/eq_core/nlp_analyzer.py
from .definitions import EMOTION_MODEL, SENTIMENT_MODEL
=======
from huggingface_hub import InferenceClient
from concurrent.futures import ThreadPoolExecutor
from .constants import EMOTION_MODEL, SENTIMENT_MODEL
>>>>>>> adb8920347ad8e4a556b8494681a66789dd80096:backend/eq_engine/emotion_analyzer.py

HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Initialize the official HuggingFace Client
# This client handles network routing, retries, and DNS internally much better than raw requests
client = InferenceClient(token=HF_TOKEN)

def _query_emotion(text: str) -> list:
    """Queries the emotion model."""
    try:
        # returns a list of TextClassificationOutputElement
        results = client.text_classification(text, model=EMOTION_MODEL)
        return [{"label": res.label, "score": res.score} for res in results]
    except Exception as e:
        print(f"[HF API] Error with Emotion Model: {e}")
        # Fallback to prevent crash
        return [{"label": "neutral", "score": 1.0}]

def _query_sentiment(text: str) -> list:
    """Queries the sentiment model."""
    try:
        results = client.text_classification(text, model=SENTIMENT_MODEL)
        return [{"label": res.label, "score": res.score} for res in results]
    except Exception as e:
        print(f"[HF API] Error with Sentiment Model: {e}")
        # Fallback to prevent crash
        return [{"label": "POSITIVE", "score": 0.5}]

def calculate_semantic_richness(text: str) -> float:
    """
    A simple heuristic for semantic richness.
    Returns a score between 0.0 and 1.0 based on vocabulary variety and sentence structure.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
        
    unique_words = set(words)
    lexical_diversity = len(unique_words) / len(words)
    
    length_bonus = min(len(words) / 100.0, 1.0)
    richness = (lexical_diversity * 0.6) + (length_bonus * 0.4)
    return min(richness, 1.0)


def analyze_text(text: str) -> dict:
    """
    Passes the user's text response through HuggingFace Inference API.
    Uses ThreadPoolExecutor to run both API calls concurrently to save time.
    """
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_emo = executor.submit(_query_emotion, text)
        future_sent = executor.submit(_query_sentiment, text)
        
        emo_results = future_emo.result()
        sent_results = future_sent.result()
    
    emotion_scores = {item['label']: item['score'] for item in emo_results}
    
    if not emotion_scores:
        emotion_scores = {"neutral": 1.0}
        
    primary_emotion = max(emotion_scores, key=emotion_scores.get)
    primary_emotion_score = emotion_scores[primary_emotion]
    
    if sent_results:
        sentiment_label = sent_results[0]['label']
        sentiment_score = sent_results[0]['score']
    else:
        sentiment_label = "POSITIVE"
        sentiment_score = 0.5
    
    intensity = primary_emotion_score
    if primary_emotion == "neutral":
        intensity = 1.0 - primary_emotion_score
        
    emotional_intensity = (intensity * 0.7) + (sentiment_score * 0.3)
    richness = calculate_semantic_richness(text)
    
    return {
        "emotion_detected": primary_emotion,
        "emotion_scores": emotion_scores,
        "sentiment_label": sentiment_label,
        "sentiment_score": sentiment_score,
        "emotional_intensity": min(emotional_intensity, 1.0),
        "semantic_richness": richness
    }
