from django.urls import path
from archive import views


upload_image = views.ImageUploadViewSet.as_view({
    'put': 'update'
})

predict = views.ImagePredictionViewSet.as_view({
    'put': 'update'
})

urlpatterns = [
    path('list', views.ArchiveList.as_view()),
    path('detail/<int:id>/', views.ArchiveDetail.as_view()),
    path('image_list/<int:archive_id>/', views.ImageList.as_view()),
    path('image_detail/<int:id>/', views.ImageDetail.as_view()),
    path('image_detail/upload_image/<int:id>/', upload_image),
    path('image_detail/predict/<int:id>/', predict),
]
