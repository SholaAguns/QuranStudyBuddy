from django.urls import path
from . import views


app_name = "quran"

urlpatterns = [
    path('', views.ChapterList.as_view(), name='chapter_list'),
    path('chapter/<int:pk>/', views.ChapterDetail.as_view(), name='chapter_detail'),
    path('verse/<int:pk>/', views.VerseDetail.as_view(), name='verse_detail'),
    path('populate_chapters/', views.populate_chapters, name='populate_chapters'),
    path('populate_verses/', views.populate_verses, name='populate_verses'),
    path('populate_editions/', views.populate_audio_editions, name='populate_audio_editions'),
    path('populate_hosted_audio/', views.populate_hosted_audio, name='populate_hosted_audio'),
    path('audio_editions/', views.AudioEditionList.as_view(), name='audio_edition_list'),
    path('audio_edition/<int:pk>/', views.AudioEditionDetail.as_view(), name='audio_edition_detail'),
    path('admin/', views.QuranAdmin.as_view(), name='admin'),
]