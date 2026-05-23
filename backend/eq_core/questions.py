"""
Question Generator - creates EQ questions tied to a generated scenario.
"""
import random

from .definitions import EQ_DIMENSIONS, SCENARIO_DIMENSION_MAP


QUESTION_TEMPLATES = {
    "self_awareness": "What emotions would you notice in yourself first, and what might those emotions tell you about your needs or triggers?",
    "self_regulation": "How would you keep your first reaction from turning into an impulsive response?",
    "empathy": "What might the other people in this situation be feeling or protecting, and how would you show that you understand them?",
    "social_skills": "What would you say or do to keep the conversation constructive and preserve trust?",
    "motivation": "What personal goal or value would help you stay engaged instead of withdrawing from the situation?",
}


def _select_dimensions(scenario_type: str, count: int) -> list[str]:
    primary_dims = SCENARIO_DIMENSION_MAP.get(
        scenario_type,
        ["self_awareness", "self_regulation", "empathy"],
    )

    selected = []
    for dimension in primary_dims:
        if dimension in EQ_DIMENSIONS and dimension not in selected:
            selected.append(dimension)

    remaining = [dimension for dimension in EQ_DIMENSIONS if dimension not in selected]
    random.shuffle(remaining)
    selected.extend(remaining[: max(0, count - len(selected))])
    return selected[:count]


def generate_questions(
    scenario_type: str,
    scenario_text: str | None = None,
    count: int | None = None,
) -> list[dict]:
    """
    Generate 4-7 open-ended questions for the scoring engine.

    Each question maps to exactly one EQ dimension, so the existing scoring
    system can calculate self_awareness, self_regulation, empathy,
    social_skills, and motivation scores from user answers.
    """
    question_count = count or random.randint(4, 7)
    question_count = max(4, min(7, question_count))
    dimensions = _select_dimensions(scenario_type, question_count)

    scenario_reference = " in the scenario" if scenario_text else ""
    questions = []
    for order, dimension in enumerate(dimensions, start=1):
        question_text = QUESTION_TEMPLATES[dimension]
        if scenario_reference:
            question_text = f"Thinking about this scenario, {question_text[0].lower()}{question_text[1:]}"

        questions.append(
            {
                "eq_dimension": dimension,
                "question_text": question_text,
                "order": order,
            }
        )

    return questions
