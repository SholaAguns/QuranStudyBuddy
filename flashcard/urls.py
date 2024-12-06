from django.urls import path
from . import views


app_name = "flashcards"

urlpatterns = [
    path('', views.FlashcardSetList.as_view(), name='flashcardset_list'),
    path('create/', views.CreateFlaschcardSet.as_view(), name='add_flashcardset'),
    path('flashcardset/<int:pk>/', views.FlashcardSetDetail.as_view(), name='flashcardset_detail'),
    path('flashcardset/<int:pk>/update', views.FlashcardSetUpdate.as_view(), name='update_flashcardset'),
    path('flashcardset/<int:pk>/delete', views.DeleteFlashcardSet.as_view(), name='delete_flashcardset'),
    path('get_service_types/', views.get_service_types, name='get_service_types'),
    path('get_id_options/<str:service_type>/', views.get_id_options, name='get_id_options'),
    path('get_juz_options/<str:service_type>/', views.get_juz_options, name='get_juz_options'),
    path('get_request_types/<str:service_type>/', views.get_request_types, name='get_request_types'),
    path('get_range_options/<str:service_type>/', views.get_range_options, name='get_range_options'),
    path('get_category_options/<str:service_type>/', views.get_category_options, name='get_category_options'),
    path('submit_flashcardset_form/', views.submit_flashcardset_form, name='submit_form'),
    path('submit_flashcardset_answers/<int:pk>/', views.submit_flashcardset_answers, name='submit_answers')

]