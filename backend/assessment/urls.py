"""
Assessment app URL configuration.
All routes are prefixed with /api/ from config/urls.py.
"""
from django.urls import path
from . import views

urlpatterns = [
    # POST — Start assessment (send user details, receive scenario + questions)
    path("assessment/start/", views.start_assessment, name="start-assessment"),

    # GET — Get questions for an assessment
    path("assessment/<str:assessment_id>/questions/", views.get_questions, name="get-questions"),

    # POST — Submit all responses for analysis
    path("assessment/<str:assessment_id>/submit/", views.submit_responses, name="submit-responses"),

    # GET — Get results for a completed assessment
    path("assessment/<str:assessment_id>/results/", views.get_results, name="get-results"),

    # GET — List past assessments
    path("assessments/history/", views.get_history, name="assessment-history"),
]
