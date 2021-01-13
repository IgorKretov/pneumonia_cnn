from django.urls import path
from user import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('profile', views.UserView.as_view()),
    path('password_change', views.PasswordChangeView.as_view()),
]
