from django.contrib import admin
from .models import UserAssessment, Scenario, Question, Response, Result

@admin.register(UserAssessment)
class UserAssessmentAdmin(admin.ModelAdmin):
    list_display = ("name", "profession", "age", "overall_eq_score", "eq_level", "is_completed", "created_at")
    list_filter = ("is_completed", "eq_level", "gender", "profession_group")
    search_fields = ("name", "profession")
    readonly_fields = ("id", "created_at", "completed_at")

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ("scenario_type", "profession_group", "difficulty", "assessment")
    list_filter = ("scenario_type", "profession_group", "difficulty")
    search_fields = ("scenario_text",)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("order", "eq_dimension", "scenario")
    list_filter = ("eq_dimension",)
    search_fields = ("question_text",)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("question", "assessment", "emotion_detected", "sentiment_label", "is_valid")
    list_filter = ("emotion_detected", "sentiment_label", "is_valid")
    search_fields = ("user_answer",)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("assessment", "overall_eq_score")
    search_fields = ("assessment__name",)
