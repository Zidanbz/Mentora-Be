# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # URL untuk aplikasi accounts akan ditambahkan di sini nanti
    path('register/', views.register_view, name='register'),
    path(
        'login/', 
        LoginView.as_view(template_name='accounts/login.html'), 
        name='login'
    ),
     path(
        'logout/', 
        LogoutView.as_view(), 
        name='logout'
    ),
]