from django.urls import path
from core import views

urlpatterns = [
    path('archives/', views.ArchiveList.as_view()),
    path('images/', views.ImageList.as_view()),
    path('images/<int:pk>/', views.ImageDetail.as_view()),
]
