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


from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core import serializers as core_serializer

from .models import User, Student,Teacher
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer


def registration_view(request):
	"""
	Registration view to every user.
	"""
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
@api_view(["GET"])
def home(request):

	"""
	Get all students and Teacher list separately
	"""
	context = {}

	students = Student.objects.all()
	students_json_list = core_serializer.serialize('json', list(students), fields = ("user.username", "user.email", "address", "standard", "favourite_subject"))
	student_list = json.loads(students_json_list)
	context["students"] = student_list

	teachers = Teacher.objects.all()
	teacher_json_list = core_serializer.serialize('json', list(teachers), fields=("user.username", "user.email", "address", "favourite_subject"))
	teacher_list = json.loads(teacher_json_list)
	context["teachers"] = teacher_list


	return render(request, 'app/home.html', context )




@login_required
@admin_only_decoratory
@api_view(["GET"])
def Get_Users(request):
	"""
	list all users in the databse
	"""
	users = User.objects.all()
	serializer = UserSerializer(users, many=True)
	return Response(serializer.data)


@login_required
@api_view(["GET"])
def Student_Get_List(request):
	"""
	List all students view
	"""
	if request.method == "GET":
		students = Student.objects.all()
		serializer = StudentSerializer(students, many=True)
		return Response(serializer.data)
		# return render(request, 'app/students.html')

@login_required
@api_view(["GET"])
def Student_Get_detail(request):
	try:
		student_obj = Student.objects.get(pk = pk)
	except Student.DoesNotExist:
		return Response(status= status.HTTP_404_NOT_FOUND)


	if request.method == "GET":
		serializer = StudentSerializer(student_obj)
		return Response(serializer.data)


@login_required
@api_view(["GET"])
def Teacher_Get_detail(request, pk):
	try:
		teacher_obj = Teacher.objects.get(pk = pk)
	except Student.DoesNotExist:
		return Response(status= status.HTTP_404_NOT_FOUND)


	if request.method == "GET":
		serializer = TeacherSerializer(student_obj)
		return Response(serializer.data)


@login_required
@api_view(["GET"])
def Teacher_Get_List(request):
	"""
	List all Teachers view
	"""
	if request.method == "GET":
		teachers = Teacher.objects.all()
		serializer = TeacherSerializer(teachers, many=True)
		return Response(serializer.data)
		# return render(request, 'app/students.html')



@login_required
@allowed_users( allowed_roles = ['admin', 'teachers','students'])
@api_view(["GET", "POST"])
def Student_Get_Post_list(request):
	"""
	List all student or create a student
	"""
	if request.method == "GET":
		students = Student.objects.all()
		serializer = StudentSerializer(students, many=True)
		return Response(serializer.data)
		# return render(request, 'app/students.html')

	elif request.method == "POST":
		serializer = StudentSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@allowed_users( allowed_roles = ['admin', 'teachers'])
@api_view(["GET", "POST"])
def Teacher_Get_Post_list(request):
	"""
	List all Teachers or create a Teacher
	"""
	if request.method == "GET":
		teachers = Teacher.objects.all()
		serializer = TeacherSerializer(teachers, many=True)
		return Response(serializer.data)
		# return render(request, 'app/teachers.html')

	elif request.method == "POST":
		serializer = TeacherSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@allowed_users(allowed_roles=["admin", "teachers"])
@api_view(["GET", "PUT", "DELETE"])
def Student_detail(request,pk):
	"""
	Update , Retrieve , Delete a specific Student object
	"""
	try:
		student_obj = Student.objects.get(pk = pk)
	except Student.DoesNotExist:
		return Response(status= status.HTTP_404_NOT_FOUND)


	if request.method == "GET":
		serializer = StudentSerializer(student_obj)
		return Response(serializer.data)

	elif request.method == "PUT":
		serializer = StudentSerializer(student_obj, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == "DELETE":
		student_obj.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
@admin_only_decoratory
@api_view(["GET", "PUT", "DELETE"])
def Teacher_detail(request,pk):
	"""
	Update , Retrieve , Delete a specific Teacher object
	"""
	try:
		teacher_obj = Teacher.objects.get(pk = pk)
	except Teacher.DoesNotExist:
		return Response(status= status.HTTP_404_NOT_FOUND)


	if request.method == "GET":
		serializer = TeacherSerializer(teacher_obj)
		return Response(serializer.data)

	elif request.method == "PUT":
		serializer = TeacherSerializer(teacher_obj, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == "DELETE":
		teacher_obj.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)




@login_required
@allowed_users(allowed_roles = ["admin","teachers"])
def get_teachers(request):
		return render(request, 'app/teachers.html')


