from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm

from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only_decoratory


def registration_view(request):
	context = {}
	form = RegistrationForm()

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			if form.cleaned_data.get('is_student'):
				group = Group.objects.filter(name="students")
				user.groups.add(group)
				print("added to students Group")

			if form.cleaned_data['is_teacher']:
				group = Group.objects.filter(name = "teachers")
				user.groups.add(group)
				print("added to teachers Group")

			messages.success(request, f"Account was created for {user}")
			return redirect('login')
	else:
		context['form'] = form
		return render(request, 'app/register.html', context)


@login_required
@allowed_users( allowed_roles = ['admin', 'teachers','students'])
def get_students(request):
	return render(request, 'app/students.html')


@login_required
@allowed_users(allowed_roles =["teachers", "admin"])
def Create_Student(request):
	pass
	




@login_required
@allowed_users(allowed_roles = ["admin","teachers"])
def get_teachers(request):
		return render(request, 'app/teachers.html')



@login_required
def home(request):
	return render(request, 'app/home.html')
