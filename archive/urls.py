from django.urls import path
from archive import views


app_name = 'archive'

upload_image = views.ImageUploadViewSet.as_view({
    'put': 'update'
})

predict = views.ImagePredictionViewSet.as_view({
    'put': 'update'
})

urlpatterns = [
    path('list', views.ArchiveList.as_view(), name='list'),
    path('detail/<int:id>/', views.ArchiveDetail.as_view(), name='detail'),
    path(
        'image_list/<int:archive_id>/',
        views.ImageList.as_view(),
        name='image-list'),
    path(
        'image_detail/<int:id>/',
        views.ImageDetail.as_view(),
        name='image-detail'),
    path(
        'image_detail/upload_image/<int:id>/',
        upload_image,
        name='image-upload'),
    path(
        'image_detail/predict/<int:id>/',
        predict,
        name='image-predict'),
]
