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
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.home, name='home'),
	path('students/', views.Student_Get_List, name='students'),
	path('teachers/', views.Teacher_Get_detail, name='teachers'),

	path('register/', views.registration_view, name='register'),
	path('login/',
		auth_views.LoginView.as_view(template_name = 'app/login.html'),
		name='login'
		),
	path('logout/',
		auth_views.LogoutView.as_view(template_name = 'app/logout.html'),
		name='logout'
		),
	path('password-reset/',
		auth_views.PasswordResetView.as_view(template_name = 'app/password_reset.html'),
		name='password_reset'
		),
	path('password-reset/done/',
		auth_views.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'),
		name='password_reset_done'
		),
	path('password-reset-confirm/<uidb64>/<token>/',
		auth_views.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html'),
		name='password_reset_confirm'
		),
	path('password-reset-complete/',
		auth_views.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'),
		name='password_reset_complete'
		),


	# JWT urls implementation
	path('api/token/', obtain_jwt_token),
	path('api/token/verify/', verify_jwt_token),
	path('api/token/refresh/', refresh_jwt_token),
	

]




