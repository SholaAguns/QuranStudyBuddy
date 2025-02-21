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
    path('chapter/<int:pk>/wordlist', views.ChapterWordList.as_view(), name='chapter_word_list'),
    path('verse_selection/<int:pk>', views.VerseSelectionDetail.as_view(), name='verse_selection_detail'),
    path('create_verse_selection', views.create_verse_selection, name='create_verse_selection'),
    path('verse_selections', views.VerseSelectionList.as_view(), name='verse_selection_list'),
    path('verse_selection/<int:pk>/delete', views.DeleteVerseSelection.as_view(), name='delete_verse_selection'),
    path('verse_selection/<int:pk>/update', views.update_verse_selection, name='update_verse_selection'),
    path('verse_selections/delete', views.delete_verse_selections, name='delete_verse_selections'),
    path('verse_selection/form', views.CreateVerseSelection.as_view(), name='verse_selection_form'),
    path('verse_selection/<int:pk>/word_list', views.VerseSelectionWordList.as_view(), name='verse_selection_word_list')
]
