from django.urls import path
from . import views


app_name = "quran"

urlpatterns = [
    path('', views.ChapterList.as_view(), name='chapter_list'),
    path('chapter/<int:pk>/', views.ChapterDetail.as_view(), name='chapter_detail'),
    path('verse/<int:pk>/', views.VerseDetail.as_view(), name='verse_detail'),
    path('populate_chapters/', views.populate_chapters, name='populate_chapters'),
    path('populate_verses/', views.populate_verses, name='populate_verses'),
    path('admin/', views.QuranAdmin.as_view(), name='admin'),
]