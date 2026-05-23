"""
Scenario Generator - creates profession-aware EQ assessment content.
"""
import random

from .definitions import PROFESSION_GROUPS, SCENARIO_TYPES
from .ai_generator import generate_llm_assessment
from .questions import generate_questions


FALLBACK_PRESSURES = {
    "technical": [
        "a critical deployment you approved has begun rolling back in production, "
        "users are flooding support channels, and two engineers on your team are "
        "openly disagreeing in the incident chat about whether to push a hotfix or "
        "revert completely—both are looking to you to break the tie",
        "during a cross-team architecture review, a senior staff engineer interrupts "
        "your proposal mid-sentence, calls the design 'naïve,' and redirects the "
        "conversation—several junior engineers who supported your idea go silent",
        "a feature you championed and personally shepherded through three sprints "
        "crashes within minutes of launch; the post-mortem channel is already active, "
        "a teammate has tagged you asking 'who signed off on this?', and your manager "
        "has scheduled an urgent one-on-one",
    ],
    "medical": [
        "you arrive for your shift and discover that the outgoing nurse's handoff notes "
        "are incomplete—a patient's medication was adjusted overnight but no rationale "
        "was documented, the patient is anxious, and the attending physician is unreachable",
        "a patient's spouse confronts you at the bedside, voice shaking, insisting that "
        "a different treatment should have been tried first—your colleague beside you "
        "stays quiet, and the rest of the care team is watching how you respond",
        "you notice that a respected colleague has charted a dosage you believe is "
        "incorrect for a vulnerable patient; when you raise it privately, they dismiss "
        "your concern and say you're 'overreacting'—the next medication round is in "
        "twenty minutes",
    ],
    "education": [
        "a parent storms into the front office demanding to speak with you, claiming "
        "in front of two other parents and the school receptionist that you singled "
        "their child out unfairly—the student is standing right there, visibly upset",
        "midway through a lesson, a student you've been quietly worried about breaks "
        "down crying and can't explain why; twenty-eight other students are watching, "
        "your co-teacher is absent today, and a classroom observation is happening in "
        "fifteen minutes",
        "a colleague who shares your grade-level curriculum rewrites key sections of "
        "a unit plan you spent weeks refining—without telling you—and the revised "
        "version has already been distributed to students the morning of a major "
        "assessment",
    ],
    "management": [
        "two of your highest-performing team members are in an escalating disagreement "
        "that has spilled into a public Slack channel—other team members are picking "
        "sides, a client deliverable is due in forty-eight hours, and HR has just "
        "pinged you asking for context",
        "in an all-hands meeting, a senior VP puts your team's quarterly results on "
        "screen and calls the numbers 'disappointing'—your team members are in the "
        "audience, several look stunned, and you have been given no advance warning",
        "an employee you recently promoted requests a private meeting and tells you "
        "that your feedback in last week's review left them feeling humiliated, that "
        "they've started looking at other opportunities, and that others on the team "
        "feel the same way but won't say it",
    ],
    "creative": [
        "a client watches your final presentation, pauses for a long moment, and says "
        "the direction 'doesn't feel right'—they question whether you truly understood "
        "the brief, and your creative director, who praised the work yesterday, stays "
        "silent",
        "during a team showcase, a collaborator presents a concept you originated as "
        "entirely their own—your name appears nowhere in the credits, leadership is "
        "visibly impressed, and the collaborator is sitting two seats away from you",
        "at 6 PM on a Friday, a stakeholder sends extensive revision notes that "
        "effectively undo two weeks of work on a campaign launching Monday morning—"
        "your team has already moved on to other projects, and the stakeholder's tone "
        "implies this should have been caught earlier",
    ],
    "general": [
        "in a team meeting, a colleague presents a proposal built on research and "
        "ideas you shared with them privately last month—others congratulate them, "
        "your manager nods approvingly, and no one seems aware of your contribution",
        "you discover that a decision directly affecting your role and workload was "
        "made in a meeting you were not invited to—when you ask about it, you're "
        "told the decision is final and implementation starts tomorrow",
        "a project you've spent months preparing unravels during a high-visibility "
        "presentation—a key assumption turns out to be wrong, the room goes quiet, "
        "and your manager asks you to 'walk us through what happened' in front of "
        "the entire leadership team",
    ],
}


def map_profession_to_group(profession: str) -> str:
    """Map a free-text profession to one of the configured profession groups."""
    if not profession:
        return "general"

    profession_lower = profession.lower().strip()

    for group, titles in PROFESSION_GROUPS.items():
        if profession_lower in titles:
            return group

        profession_words = set(profession_lower.split())
        for title in titles:
            if profession_words.intersection(title.split()):
                return group

    return "general"


def _difficulty_for_age(age: int) -> str:
    if age < 22:
        return "medium"
    if age >= 35:
        return "hard"
    return random.choice(["medium", "hard"])


def _fallback_scenario(profession: str, age: int, group: str) -> dict:
    """
    Local backup used when the LLM is not configured.

    It still creates a fresh scenario from age/profession instead of returning a
    fixed pre-built scenario.
    """
    difficulty = _difficulty_for_age(age)
    pressure = random.choice(FALLBACK_PRESSURES.get(group, FALLBACK_PRESSURES["general"]))
    scenario_type = random.choice(SCENARIO_TYPES)
    career_stage = "early-career" if age < 25 else "experienced" if age >= 35 else "mid-career"
    profession_label = profession.strip() if profession else "professional"

    scenario_text = (
        f"You are a {career_stage} {profession_label}. It has already been a "
        f"long and demanding day when {pressure}. The room feels tense—people are "
        "watching, some waiting for your lead and others bracing for a misstep. "
        "Your heart rate is up and you can feel the weight of the moment. What you "
        "do in the next few minutes will shape how others see your judgment, whether "
        "key relationships strengthen or fracture, and how you feel about yourself "
        "when the day is over. You must read the emotions in the room, manage your "
        "own internal reaction, choose your words carefully, and find a path forward "
        "even if things don't go the way you planned."
    )

    return {
        "scenario_text": scenario_text,
        "scenario_type": scenario_type,
        "profession_group": group,
        "difficulty": difficulty,
        "questions": generate_questions(scenario_type, scenario_text=scenario_text, count=7),
    }


def generate_scenario(profession: str, age: int) -> dict:
    """
    Generate a personalized scenario and 4-7 questions from the user's profile.

    LLM generation is used when LLM_API_KEY or OPENAI_API_KEY is configured.
    Otherwise the system uses a local dynamic fallback so development remains
    usable offline.
    """
    group = map_profession_to_group(profession)
    llm_payload = generate_llm_assessment(profession, age, group)
    if llm_payload:
        return llm_payload

    return _fallback_scenario(profession, age, group)
