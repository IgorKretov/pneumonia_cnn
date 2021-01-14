from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('archive', views.archive),
    path('archive/create', views.archive_create),
    path('archive/list', views.archive_list),
    path('archive/<int:id>/', views.archive_images),
]
