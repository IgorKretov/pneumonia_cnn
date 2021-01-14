from django.urls import path
from archive import views

urlpatterns = [
    path('list', views.ArchiveList.as_view()),
    path('detail/<int:id>/', views.ArchiveDetail.as_view()),
    path('image_list/<int:archive_id>/', views.ImageList.as_view()),
    path('image_detail/<int:id>/', views.ImageDetail.as_view()),
]
