from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile', views.UserView.as_view(), name='profile'),
    path(
        'password_change',
        views.PasswordChangeView.as_view(),
        name='password_change'),
]
