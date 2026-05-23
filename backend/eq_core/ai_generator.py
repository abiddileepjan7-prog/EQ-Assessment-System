"""
LLM client for adaptive EQ assessment generation.

The client uses an OpenAI-compatible chat completions endpoint when an API key
is configured. If no key is present, callers can fall back to deterministic
local generation.
"""
import json
import os
import re
import urllib.error
import urllib.request

from .definitions import EQ_DIMENSIONS, EQ_DIMENSION_DESCRIPTIONS, SCENARIO_TYPES

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()


DEFAULT_API_BASE = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("LLM response did not contain a JSON object.")

    return json.loads(cleaned[start : end + 1])


def _normalize_generated_payload(payload: dict, profession_group: str) -> dict:
    scenario_type = payload.get("scenario_type", "workplace_conflict")
    if scenario_type not in SCENARIO_TYPES:
        scenario_type = "workplace_conflict"

    difficulty = payload.get("difficulty", "medium")
    if difficulty not in {"easy", "medium", "hard"}:
        difficulty = "medium"

    questions = []
    used_dimensions = set()
    for raw_question in payload.get("questions", []):
        dimension = raw_question.get("eq_dimension")
        question_text = raw_question.get("question_text", "").strip()
        if dimension not in EQ_DIMENSIONS or not question_text:
            continue
        if dimension in used_dimensions:
            continue

        questions.append(
            {
                "eq_dimension": dimension,
                "question_text": question_text,
                "order": len(questions) + 1,
            }
        )
        used_dimensions.add(dimension)

        if len(questions) == 7:
            break

    if len(questions) < 4:
        raise ValueError("LLM response did not include enough valid questions.")

    scenario_text = payload.get("scenario_text", "").strip()
    if len(scenario_text) < 80:
        raise ValueError("LLM response did not include a useful scenario.")

    return {
        "scenario_text": scenario_text,
        "scenario_type": scenario_type,
        "profession_group": profession_group,
        "difficulty": difficulty,
        "questions": questions,
    }


def generate_llm_assessment(profession: str, age: int, profession_group: str) -> dict | None:
    """
    Generate one personalized scenario and 4-7 EQ questions.

    Returns None when the LLM is not configured or unavailable so callers can
    keep the assessment flow working with a local fallback.
    """
    api_key = (
        os.getenv("LLM_API_KEY")
        or os.getenv("GROQ_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if not api_key:
        return None

    api_base = os.getenv("LLM_API_BASE", DEFAULT_API_BASE).rstrip("/")
    model = os.getenv("LLM_MODEL", DEFAULT_MODEL)
    timeout = int(os.getenv("LLM_TIMEOUT_SECONDS", "30"))

    dimensions = "\n".join(
        f"- {dimension}: {EQ_DIMENSION_DESCRIPTIONS[dimension]}"
        for dimension in EQ_DIMENSIONS
    )

    prompt = f"""
Create a personalized emotional intelligence assessment for this user:
- Age: {age}
- Profession: {profession or "general professional"}
- Profession group: {profession_group}

Generate exactly one realistic workplace, school, career, or life scenario that
fits the user's age and profession. The scenario should be emotionally
challenging but safe, non-graphic, culturally neutral, and answerable by a user
without specialized legal or medical knowledge.

Then create 4 to 7 open-ended questions based on that same scenario. Each
question must assess exactly one of these EQ dimensions:
{dimensions}

Return only valid JSON with this shape:
{{
  "scenario_type": "one of {SCENARIO_TYPES}",
  "difficulty": "easy|medium|hard",
  "scenario_text": "120-220 words, second person, specific to age/profession",
  "questions": [
    {{
      "eq_dimension": "one of {EQ_DIMENSIONS}",
      "question_text": "open-ended question tied to the scenario"
    }}
  ]
}}

Rules:
- Use 4 to 7 questions.
- Do not repeat an eq_dimension.
- Prefer a balanced spread across self_awareness, self_regulation, empathy,
  social_skills, and motivation.
- Do not include scoring, answers, advice, markdown, or explanations.
""".strip()

    request_body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You generate psychometrically useful EQ assessment content as strict JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
            "response_format": {"type": "json_object"},
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        f"{api_base}/chat/completions",
        data=request_body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw_response = response.read().decode("utf-8")
        response_data = json.loads(raw_response)
        content = response_data["choices"][0]["message"]["content"]
        payload = _extract_json(content)
        return _normalize_generated_payload(payload, profession_group)
    except (KeyError, ValueError, json.JSONDecodeError, urllib.error.URLError):
        return None
