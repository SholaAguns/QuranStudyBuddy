from django.urls import path
from . import views


app_name = "scorecard"

urlpatterns = [
    path('<int:pk>/', views.ScorecardDetail.as_view(), name='scorecard_detail'),
    path('create/admin', views.CreateScorecard.as_view(), name='manual_scorecard_creation'),
    path('update', views.scorecard_manual_update, name='manual_scorecard_update'),
    path('update/stats', views.update_scorecard_stats, name='update_scorecard_stats'),
    path('get_verse_stats/', views.get_verse_stats, name='get_verse_stats'),
    path('get_phrase_stats/', views.get_phrase_stats, name='get_phrase_stats'),
    path('get_verse_selection_stats/', views.get_verse_selection_stats, name='get_verse_selection_stats'),
    path('get_word_stats/', views.get_word_stats, name='get_word_stats'),
    ]