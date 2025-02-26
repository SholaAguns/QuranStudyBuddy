from django.urls import path
from . import views


app_name = "scorecard"

urlpatterns = [
    path('<int:pk>/', views.ScorecardDetail.as_view(), name='scorecard_detail'),
    path('create/admin', views.CreateScorecard.as_view(), name='manual_scorecard_creation'),
    path('update', views.scorecard_manual_update, name='manual_scorecard_update'),
    path('update/stats', views.update_scorecard_stats, name='update_scorecard_stats'),
    ]