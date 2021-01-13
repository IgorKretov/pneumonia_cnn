from django.urls import path
from archive import views

urlpatterns = [
    path('list', views.ArchiveList.as_view()),
    path('detail/<int:id>/', views.ArchiveDetail.as_view()),
    path('image/list', views.ImageList.as_view()),
    path('image/detail/<int:id>/', views.ImageDetail.as_view()),
]
