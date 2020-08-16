from django.contrib.auth.forms import UserCreationForm
from django import forms

from app.models import User

class RegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['email', 'username', 'password1', 'password2','is_student','is_teacher']


# If required separate forms for student and teacher
class StudentSignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["email", "username", "password1", "password2"]

class TeacherSignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["email", "username", "password1", "password2"]

