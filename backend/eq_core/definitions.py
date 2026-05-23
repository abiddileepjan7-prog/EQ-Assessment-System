"""
definitions.py — Core definitions for the EQ Assessment System.

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
# The 5 core competencies drawn from established emotional
# intelligence frameworks (Goleman, Bar-On, Salovey-Mayer).
# Each user response is scored across these dimensions.
# ============================================================

EQ_DIMENSIONS = [
    "self_awareness",
    "self_regulation",
    "empathy",
    "social_skills",
    "motivation",
]

EQ_DIMENSION_DESCRIPTIONS = {
    "self_awareness": (
        "The ability to accurately recognize your own emotions as they occur, "
        "understand how they influence your thoughts and behavior, and maintain "
        "a realistic assessment of your strengths and limitations"
    ),
    "self_regulation": (
        "The capacity to manage disruptive emotions and impulses, stay composed "
        "under pressure, think before acting, and adapt your emotional responses "
        "to suit the demands of different situations"
    ),
    "empathy": (
        "The skill of sensing what other people are feeling, understanding their "
        "perspective even when it differs from your own, and responding with "
        "appropriate care, curiosity, and emotional attunement"
    ),
    "social_skills": (
        "Effectiveness in managing relationships, communicating clearly, "
        "influencing and inspiring others, navigating conflict constructively, "
        "and building cooperative bonds across diverse groups"
    ),
    "motivation": (
        "An inner drive to pursue goals with energy and persistence, to embrace "
        "challenges as growth opportunities, to recover from setbacks without "
        "losing commitment, and to maintain optimism in the face of difficulty"
    ),
}


# ============================================================
# 2. SCENARIO TYPES
# 8 categories of emotionally challenging situations the system
# generates. Each type probes a distinct combination of the
# 5 core EQ dimensions.
# ============================================================

SCENARIO_TYPES = [
    "interpersonal_conflict",
    "public_criticism",
    "leadership_under_pressure",
    "team_setback",
    "ethical_tension",
    "high_stakes_decision",
    "trust_violation",
    "unexpected_failure",
]

# Which EQ dimensions each scenario type primarily activates.
# The first dimension listed carries the heaviest weight in scoring.
SCENARIO_DIMENSION_MAP = {
    "interpersonal_conflict": ["social_skills", "self_regulation", "empathy"],
    "public_criticism": ["self_regulation", "self_awareness", "motivation"],
    "leadership_under_pressure": ["social_skills", "self_regulation", "motivation"],
    "team_setback": ["empathy", "motivation", "social_skills"],
    "ethical_tension": ["self_awareness", "empathy", "motivation"],
    "high_stakes_decision": ["self_regulation", "self_awareness", "social_skills"],
    "trust_violation": ["empathy", "self_awareness", "social_skills"],
    "unexpected_failure": ["motivation", "self_regulation", "self_awareness"],
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
# Keywords and natural-language patterns that signal higher or
# lower competency in each EQ dimension. The scoring engine
# scans user responses for these phrases to adjust dimension
# scores alongside the NLP transformer outputs.
# ============================================================

POSITIVE_INDICATORS = {
    "self_awareness": [
        # Naming and owning internal states
        "i feel",
        "i realize",
        "i notice",
        "i recognize",
        "i'm aware",
        "i understand my",
        "reflecting on",
        "i tend to",
        "that triggered",
        "i can see how my",
        "my reaction",
        "looking inward",
        "honest with myself",
        "i was wrong",
        "my own bias",
        "i need to check myself",
    ],
    "self_regulation": [
        # Deliberate control and composure
        "stay calm",
        "take a breath",
        "pause before",
        "composed",
        "measured",
        "patient",
        "controlled",
        "think before",
        "cool down first",
        "give myself a moment",
        "step away briefly",
        "not react immediately",
        "regulate",
        "collect my thoughts",
        "respond rather than react",
        "wait until i'm ready",
    ],
    "empathy": [
        # Perspective-taking and emotional attunement
        "they might feel",
        "understand their",
        "perspective",
        "in their shoes",
        "compassion",
        "care about",
        "what they're going through",
        "how this affects them",
        "listen to their side",
        "validate their feelings",
        "acknowledge their experience",
        "must be difficult for",
        "i can see why they",
        "their point of view",
        "show them i understand",
        "emotionally present",
    ],
    "social_skills": [
        # Relationship management and communication
        "together",
        "collaborate",
        "communicate",
        "team",
        "discuss openly",
        "listen actively",
        "approach them",
        "find common ground",
        "build trust",
        "clear conversation",
        "address it directly",
        "work through this",
        "constructive feedback",
        "hear everyone out",
        "mediate",
        "bridge the gap",
        "resolve this together",
        "de-escalate",
    ],
    "motivation": [
        # Drive, resilience, and growth orientation
        "learn from this",
        "opportunity",
        "grow",
        "improve",
        "challenge",
        "keep going",
        "move forward",
        "not give up",
        "persist",
        "bounce back",
        "setback is temporary",
        "what can i take from this",
        "do better next time",
        "use this as fuel",
        "stay focused on the goal",
        "long-term perspective",
        "committed to",
        "overcome",
    ],
}

NEGATIVE_INDICATORS = {
    "self_awareness": [
        # Emotional blindness and deflection
        "don't know why",
        "no idea",
        "whatever",
        "don't care",
        "it doesn't matter",
        "i'm fine",
        "not my problem",
        "has nothing to do with me",
        "i don't have feelings about",
        "i never do that",
        "that's just how i am",
    ],
    "self_regulation": [
        # Impulsive and uncontrolled reactions
        "explode",
        "yell",
        "snap",
        "lose it",
        "furious",
        "can't control",
        "lash out",
        "tell them off",
        "slam",
        "blow up",
        "storm out",
        "say something i'll regret",
        "scream",
        "go off on",
        "lose my temper",
    ],
    "empathy": [
        # Dismissal and blame
        "their fault",
        "blame them",
        "they deserve",
        "don't care about them",
        "not my problem",
        "they should have",
        "too bad for them",
        "they brought it on themselves",
        "why should i care",
        "that's their issue",
        "they're overreacting",
        "being too sensitive",
        "get over it",
    ],
    "social_skills": [
        # Withdrawal and avoidance
        "alone",
        "avoid",
        "ignore them",
        "don't talk",
        "isolate",
        "shut them out",
        "not my job to fix",
        "let them figure it out",
        "stay out of it",
        "keep to myself",
        "ghost",
        "cut them off",
        "refuse to engage",
    ],
    "motivation": [
        # Defeat and surrender
        "give up",
        "pointless",
        "why bother",
        "don't care",
        "no point",
        "quit",
        "can't do this",
        "hopeless",
        "never going to work",
        "waste of time",
        "what's the use",
        "too late",
        "doesn't matter anymore",
        "i'm done",
        "nothing will change",
    ],
}


# ============================================================
# 6. SCORE INTERPRETATION
# Maps overall EQ score ranges to three levels: Low, Average,
# and High. Each level includes a description and actionable
# guidance for the user.
# ============================================================

SCORE_LEVELS = [
    {
        "range": (0, 40),
        "level": "Low EQ",
        "key": "low",
        "description": (
            "Your responses suggest significant room for growth in emotional "
            "intelligence. You may find it difficult to identify your own emotions "
            "in the moment, read the feelings of others accurately, or regulate "
            "impulsive reactions under pressure. This is a starting point, not a "
            "ceiling — targeted practice in self-reflection, active listening, and "
            "stress management can produce meaningful improvement."
        ),
    },
    {
        "range": (41, 70),
        "level": "Average EQ",
        "key": "average",
        "description": (
            "You demonstrate a functional level of emotional intelligence with "
            "clear strengths in some areas. You can often recognize your emotions "
            "and show empathy, but may struggle with consistency — particularly "
            "under high stress, conflict, or ambiguity. Focused development in "
            "your weaker dimensions can elevate your interpersonal effectiveness "
            "and decision-making."
        ),
    },
    {
        "range": (71, 100),
        "level": "High EQ",
        "key": "high",
        "description": (
            "Your responses reflect strong emotional intelligence across multiple "
            "dimensions. You show a well-developed ability to understand your own "
            "emotional patterns, attune to others with genuine empathy, stay "
            "composed under pressure, communicate constructively, and maintain "
            "motivation through setbacks. Continue applying these skills and "
            "consider mentoring others in emotional competency."
        ),
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
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
