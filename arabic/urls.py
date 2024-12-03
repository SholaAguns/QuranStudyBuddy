from django.urls import path
from . import views


app_name = "arabic"

urlpatterns = [
    path('', views.ArabicHome.as_view(), name='arabic_home'),
    path('phrases/', views.PhraseList.as_view(), name='phrase_list'),
    path('phrase/<int:pk>/', views.PhraseDetail.as_view(), name='phrase_detail'),
    path('create_phrase/', views.CreatePhrase.as_view(), name="add_phrase"),
    path('phrase/<int:pk>/update', views.PhraseUpdate.as_view(), name='update_phrase'),
    path('phrase/<int:pk>/delete', views.DeletePhrase.as_view(), name='delete_phrase'),
]