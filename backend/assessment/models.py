"""
Assessment Models — Database schema for the EQ Assessment System.

5 tables:
1. UserAssessment — stores user profile + overall results
2. Scenario       — the generated emotional scenario
3. Question       — individual EQ questions within a scenario
4. Response       — user's answer + NLP analysis for each question
5. Result         — final EQ scores across all 9 dimensions + feedback
"""
import uuid
from django.db import models


class UserAssessment(models.Model):
    """
    The top-level record for each assessment session.
    Stores user demographic info and links to everything else.

    WHY UUID? — So we can use it in URLs (/assessment/abc123/)
    without exposing auto-increment IDs (security best practice).
    """

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("non_binary", "Non-binary"),
        ("prefer_not", "Prefer not to say"),
    ]

    EQ_LEVEL_CHOICES = [
        ("low", "Low EQ"),
        ("average", "Average EQ"),
        ("high", "High EQ"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    profession = models.CharField(max_length=100)
    profession_group = models.CharField(max_length=50, blank=True)

    # These get filled AFTER analysis is complete
    overall_eq_score = models.FloatField(null=True, blank=True)
    eq_level = models.CharField(
        max_length=20, choices=EQ_LEVEL_CHOICES, blank=True
    )

    # Status tracking
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.profession} ({self.created_at:%Y-%m-%d})"


class Scenario(models.Model):
    """
    The emotionally challenging scenario presented to the user.
    Generated based on their profession group and age.

    One assessment has exactly ONE scenario.
    """

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.OneToOneField(
        UserAssessment,
        on_delete=models.CASCADE,
        related_name="scenario",
    )
    scenario_text = models.TextField()
    scenario_type = models.CharField(max_length=50)
    profession_group = models.CharField(max_length=50)
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default="medium"
    )

    def __str__(self):
        return f"[{self.scenario_type}] {self.scenario_text[:60]}..."


class Question(models.Model):
    """
    An individual EQ question generated from the scenario.
    Each question targets a specific EQ dimension.

    One scenario has 5-7 questions.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_text = models.TextField()
    eq_dimension = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Q{self.order}: [{self.eq_dimension}] {self.question_text[:50]}..."


class Response(models.Model):
    """
    User's answer to a question + NLP analysis results.

    This is where transformer model outputs get stored:
    - emotion_detected: primary emotion label (joy, anger, etc.)
    - emotion_scores: full probability distribution from the model
    - sentiment_label: POSITIVE or NEGATIVE
    - sentiment_score: confidence (0.0 to 1.0)
    - emotional_intensity: how strong the emotion is
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        related_name="response",
    )
    assessment = models.ForeignKey(
        UserAssessment,
        on_delete=models.CASCADE,
        related_name="responses",
    )

    # User's raw answer
    user_answer = models.TextField()

    # NLP Analysis Results (filled after transformer processing)
    emotion_detected = models.CharField(max_length=20, blank=True)
    emotion_scores = models.JSONField(default=dict, blank=True)
    sentiment_label = models.CharField(max_length=10, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    emotional_intensity = models.FloatField(null=True, blank=True)

    # Validation
    is_valid = models.BooleanField(default=True)
    validation_message = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Response to Q{self.question.order}: {self.user_answer[:40]}..."


class Result(models.Model):
    """
    Final EQ scores across the 5 core dimensions + AI-generated feedback.

    One assessment has exactly ONE result record.
    All scores are 0-100.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.OneToOneField(
        UserAssessment,
        on_delete=models.CASCADE,
        related_name="result",
    )

    # Per-dimension scores (0-100)
    self_awareness_score = models.FloatField(default=0)
    self_regulation_score = models.FloatField(default=0)
    empathy_score = models.FloatField(default=0)
    social_skills_score = models.FloatField(default=0)
    motivation_score = models.FloatField(default=0)

    # Aggregated
    overall_eq_score = models.FloatField(default=0)

    # AI-generated feedback (stored as JSON lists)
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    feedback_text = models.TextField(blank=True)

    def __str__(self):
        return f"Result for {self.assessment.name}: {self.overall_eq_score}/100"

