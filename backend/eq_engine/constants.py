"""
constants.py — Core definitions for the EQ Assessment System.

This file contains ALL the foundational constants used throughout the system:
- EQ dimensions (what we measure)
- Scenario types (emotional situations)
- Profession groups (how we adapt scenarios)
- Emotion labels (what NLP detects)
- Scoring indicators (how we map language → EQ scores)
- Score interpretation (what the numbers mean)
"""


# ============================================================
# 1. EQ DIMENSIONS
# The 9 psychological categories the AI evaluates.
# Each user response is scored across these dimensions.
# ============================================================

EQ_DIMENSIONS = [
    "self_awareness",
    "self_regulation",
    "empathy",
    "social_skills",
    "motivation",
    "stress_management",
    "conflict_resolution",
    "adaptability",
    "resilience",
]

EQ_DIMENSION_DESCRIPTIONS = {
    "self_awareness": "Recognizing own emotions and their impact on behavior",
    "self_regulation": "Managing disruptive emotions and impulses",
    "empathy": "Understanding and sharing the feelings of others",
    "social_skills": "Managing relationships and building networks",
    "motivation": "Inner drive to achieve beyond external rewards",
    "stress_management": "Coping effectively under pressure",
    "conflict_resolution": "Navigating disagreements constructively",
    "adaptability": "Flexibility in handling change",
    "resilience": "Bouncing back from setbacks and adversity",
}


# ============================================================
# 2. SCENARIO TYPES
# 10 categories of emotional situations the system generates.
# Each scenario tests specific EQ dimensions.
# ============================================================

SCENARIO_TYPES = [
    "workplace_conflict",
    "ethical_dilemma",
    "leadership_pressure",
    "team_failure",
    "criticism_handling",
    "emotional_loss",
    "high_pressure_decision",
    "communication_breakdown",
    "social_rejection",
    "unexpected_failure",
]

# Which EQ dimensions each scenario type primarily tests
SCENARIO_DIMENSION_MAP = {
    "workplace_conflict": ["conflict_resolution", "social_skills", "self_regulation"],
    "ethical_dilemma": ["self_awareness", "motivation", "resilience"],
    "leadership_pressure": ["stress_management", "social_skills", "motivation"],
    "team_failure": ["resilience", "empathy", "adaptability"],
    "criticism_handling": ["self_awareness", "self_regulation", "resilience"],
    "emotional_loss": ["resilience", "stress_management", "self_awareness"],
    "high_pressure_decision": ["stress_management", "adaptability", "motivation"],
    "communication_breakdown": ["social_skills", "empathy", "conflict_resolution"],
    "social_rejection": ["resilience", "self_awareness", "adaptability"],
    "unexpected_failure": ["resilience", "adaptability", "stress_management"],
}


# ============================================================
# 3. PROFESSION GROUPS
# How the AI adapts scenarios to the user's profession.
# Users type free text; we fuzzy-match into these groups.
# ============================================================

PROFESSION_GROUPS = {
    "technical": [
        "software engineer",
        "data scientist",
        "cybersecurity analyst",
        "devops engineer",
        "ml engineer",
        "web developer",
        "system administrator",
    ],
    "medical": [
        "doctor",
        "nurse",
        "therapist",
        "pharmacist",
        "paramedic",
        "psychologist",
    ],
    "education": [
        "teacher",
        "professor",
        "trainer",
        "academic researcher",
        "teaching assistant",
    ],
    "management": [
        "manager",
        "team lead",
        "hr",
        "project manager",
        "ceo",
        "cto",
        "product manager",
    ],
    "creative": [
        "designer",
        "writer",
        "artist",
        "musician",
        "content creator",
        "photographer",
    ],
    "general": [
        "student",
        "freelancer",
        "unemployed",
        "intern",
        "entrepreneur",
        "other",
    ],
}


# ============================================================
# 4. EMOTION & SENTIMENT LABELS
# Mapped to Hugging Face model outputs.
# ============================================================

# From: j-hartmann/emotion-english-distilroberta-base
EMOTIONS = [
    "anger",
    "disgust",
    "fear",
    "joy",
    "neutral",
    "sadness",
    "surprise",
]

# From: distilbert-base-uncased-finetuned-sst-2-english
SENTIMENTS = [
    "POSITIVE",
    "NEGATIVE",
]


# ============================================================
# 5. SCORING INDICATORS
# Keywords/patterns that increase or decrease EQ dimension scores.
# Used by the scoring engine to map NLP outputs → EQ scores.
# ============================================================

POSITIVE_INDICATORS = {
    "self_awareness": [
        "i feel",
        "i realize",
        "i notice",
        "i understand my",
        "i'm aware",
        "i recognize",
        "reflecting on",
    ],
    "self_regulation": [
        "stay calm",
        "take a breath",
        "pause",
        "composed",
        "measured",
        "patient",
        "controlled",
    ],
    "empathy": [
        "they might feel",
        "understand their",
        "perspective",
        "in their shoes",
        "compassion",
        "care about",
    ],
    "social_skills": [
        "together",
        "collaborate",
        "communicate",
        "team",
        "discuss",
        "listen",
        "approach them",
    ],
    "motivation": [
        "goal",
        "improve",
        "learn",
        "grow",
        "opportunity",
        "challenge",
        "strive",
        "achieve",
    ],
    "stress_management": [
        "cope",
        "manage",
        "handle",
        "breathe",
        "prioritize",
        "step back",
        "take time",
    ],
    "conflict_resolution": [
        "compromise",
        "resolve",
        "mediate",
        "find common ground",
        "both sides",
        "negotiate",
        "agree",
    ],
    "adaptability": [
        "flexible",
        "adjust",
        "adapt",
        "change approach",
        "open to",
        "pivot",
        "try different",
    ],
    "resilience": [
        "bounce back",
        "learn from",
        "move forward",
        "overcome",
        "persist",
        "keep going",
        "not give up",
    ],
}

NEGATIVE_INDICATORS = {
    "self_awareness": [
        "don't know why",
        "no idea",
        "whatever",
        "don't care",
    ],
    "self_regulation": [
        "explode",
        "yell",
        "snap",
        "lose it",
        "furious",
        "can't control",
    ],
    "empathy": [
        "their fault",
        "blame",
        "they deserve",
        "don't care about them",
        "not my problem",
    ],
    "social_skills": [
        "alone",
        "avoid",
        "ignore them",
        "don't talk",
        "isolate",
    ],
    "motivation": [
        "give up",
        "pointless",
        "why bother",
        "don't care",
        "no point",
    ],
    "stress_management": [
        "panic",
        "overwhelmed",
        "can't handle",
        "breaking down",
        "too much",
    ],
    "conflict_resolution": [
        "walk away",
        "avoid conflict",
        "not worth it",
        "they can deal with it",
    ],
    "adaptability": [
        "refuse to change",
        "always done it",
        "won't budge",
        "rigid",
        "stuck",
    ],
    "resilience": [
        "quit",
        "give up",
        "can't do this",
        "hopeless",
        "never recover",
    ],
}


# ============================================================
# 6. SCORE INTERPRETATION
# Maps overall EQ score ranges to labels and descriptions.
# ============================================================

SCORE_LEVELS = [
    {
        "range": (0, 30),
        "level": "Low EQ",
        "description": "Significant room for emotional growth. "
        "Focus on building self-awareness and empathy.",
    },
    {
        "range": (31, 50),
        "level": "Below Average",
        "description": "Some emotional awareness present but needs "
        "consistent development across multiple areas.",
    },
    {
        "range": (51, 70),
        "level": "Average EQ",
        "description": "Decent emotional intelligence with clear "
        "strengths. Targeted improvement can elevate performance.",
    },
    {
        "range": (71, 85),
        "level": "Above Average",
        "description": "Strong emotional awareness and interpersonal "
        "skills. Fine-tuning specific areas will maximize impact.",
    },
    {
        "range": (86, 100),
        "level": "Exceptional EQ",
        "description": "Outstanding emotional intelligence across "
        "all dimensions. Continue applying these strengths.",
    },
]


# ============================================================
# 7. VALIDATION CONSTANTS
# Thresholds for response validation.
# ============================================================

MIN_RESPONSE_LENGTH = 10  # Minimum characters for a valid response
MAX_RESPONSE_LENGTH = 5000  # Maximum characters
MIN_WORD_COUNT = 3  # Minimum words
SPAM_PATTERNS = [
    "asdf",
    "qwerty",
    "123",
    "idk",
    "i don't know",
    "nothing",
    "n/a",
    "na",
    "no comment",
    "test",
    "aaa",
    "bbb",
    "xxx",
    "lol",
    "lmao",
]


# ============================================================
# 8. MODEL IDENTIFIERS
# Hugging Face model names used in the NLP pipeline.
# ============================================================

EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
