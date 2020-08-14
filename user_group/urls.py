from django.contrib import admin
from django.urls import path

from app import views
from django.contrib.auth import views as auth_views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.home, name='home'),
	path('get-all-students/', views.Student_Get_List, name='get-all-students'),
	path('get-student/<int:id>/', views.Student_Get_detail, name='get-student-specific'),
	path('update-student/<int:id>/', views.Student_detail, name='update-student'),
	path('delete-student/<int:id>/', views.Student_detail, name='delete-student'),


	path('get-all-teachers/', views.Teacher_Get_List, name='get-all-teachers'),
	path('get-teacher/<int:id>/', views.Teacher_Get_detail, name='get-teacher'),
	path('update-teacher/<int:id>/', views.Teacher_detail, name='update-teacher'),
	path('delete-teacher/<int:id>/', views.Teacher_detail, name='delete-teacher'),	

	path('add-student/', views.Student_Get_Post_list, name='add-student'),
	path('add-teacher', views.Teacher_Get_Post_list, name='add-teacher'),

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
	path('api-auth/', include("rest_framewor.urls")),
	path('api/token/', obtain_jwt_token, name='obtain-token'),
	path('api/token/verify/', verify_jwt_token, name='verify-token'),
	path('api/token/refresh/', refresh_jwt_token, name='refresh-token'),
	

]


