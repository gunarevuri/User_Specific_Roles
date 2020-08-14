"""user_group URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('students/', views.get_students, name='get_students'),
    path('teachers/', views.get_teachers, name='get_teachers'),

    path('register/', views.registration_view, name='register'),
    path('login/',
        auth_views.LoginView.as_view(template_name = 'app/login.html'),
        name='login'
        ),
    path('logout/', 
        auth_views.LogoutView.as_view(template_name = 'app/logout.html'),
        name='logout'
        ),
    path('password_reset', 
        auth_views.PasswordResetView.as_view(template_name = 'app/password_templates/password_reset.html'),
        name='password_reset'
        ),
]
