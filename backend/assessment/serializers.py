"""
Assessment Serializers — Converts Django models to/from JSON.
"""
from rest_framework import serializers
from .models import UserAssessment, Scenario, Question, Response, Result


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "eq_dimension", "order"]


class ScenarioSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Scenario
        fields = ["id", "scenario_text", "scenario_type", "difficulty", "questions"]


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            "id",
            "question",
            "user_answer",
            "emotion_detected",
            "sentiment_label",
            "sentiment_score",
            "emotional_intensity",
            "is_valid",
            "validation_message",
        ]
        read_only_fields = [
            "emotion_detected",
            "sentiment_label",
            "sentiment_score",
            "emotional_intensity",
            "is_valid",
            "validation_message",
        ]


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            "overall_eq_score",
            "self_awareness_score",
            "self_regulation_score",
            "empathy_score",
            "social_skills_score",
            "motivation_score",
        ]


class UserAssessmentSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer(read_only=True)
    result = ResultSerializer(read_only=True)

    class Meta:
        model = UserAssessment
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "profession",
            "profession_group",
            "overall_eq_score",
            "eq_level",
            "is_completed",
            "created_at",
            "completed_at",
            "scenario",
            "result",
        ]
        read_only_fields = [
            "profession_group",
            "overall_eq_score",
            "eq_level",
            "is_completed",
            "created_at",
            "completed_at",
        ]
