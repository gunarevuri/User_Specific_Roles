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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core import serializers as core_serializer

from .models import User, Student,Teacher
from .serializers import StudentSerializer, TeacherSerializer, UserSerializer

from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from django.conf import Settings

# if you are already login you wont get access to this view
@unauthenticated_user
def registration_view(request):
	"""
	Before this make sure you have created superuser and added groups required.
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

			# if is_student is true in the form then assign user to student group

			if form.cleaned_data.get('is_student'):
				group = Group.objects.filter(name="students")
				user.groups.add(group)

				print("added to students Group")

			# if is_teacher is true in the form then assign user to Teacher group

			if form.cleaned_data['is_teacher']:
				group = Group.objects.filter(name = "teachers")
				user.groups.add(group)

				print("added to teachers Group")

			messages.success(request, f"Account was created for the {user}")
			return redirect('login')
	else:
		context['form'] = form
		return render(request, 'app/register.html', context)


@login_required
@permission_classes([IsAuthenticated,])
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
@permission_classes([IsAuthenticated,])
@admin_only_decoratory
@api_view(["GET"])
def Get_Users(request):
	"""
	list all users in the databse only admin can see this
	"""
	users = User.objects.all()
	serializer = UserSerializer(users, many=True)
	return Response(serializer.data)
	# return render(request, 'app/home.html', {"data":"Json Data"})


@login_required
@permission_classes([IsAuthenticated,])
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
@permission_classes([IsAuthenticated,])
@api_view(["GET"])
def Student_Get_detail(request, pk):
	"""
	Display specific student
	"""
	try:
		student_obj = Student.objects.get(pk = pk)
	except Student.DoesNotExist:
		return Response(status= status.HTTP_404_NOT_FOUND)


	if request.method == "GET":
		serializer = StudentSerializer(student_obj)
		return Response(serializer.data)


@login_required
@permission_classes([IsAuthenticated,])
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
@permission_classes([IsAuthenticated,])
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
@permission_classes([IsAuthenticated,])
@allowed_users( allowed_roles = ['admin', 'teachers'])
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
@permission_classes([IsAuthenticated,])
@admin_only_decoratory
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
@permission_classes([IsAuthenticated,])
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
		# return redirect('get-student-specific')

	elif request.method == "DELETE":
		student_obj.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		# return redirect('get-students')

@login_required
@permission_classes([IsAuthenticated,])
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
		# return redirect('update-student-specific')

	elif request.method == "DELETE":
		teacher_obj.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		# return redirect('get-all-teachers')


# If you want to create your own token token with username and any other fieds
@api_view(["POST"])
@permission_classes([AllowAny, ])
def authenticate_user(request):
	try:
		username = request.data['username']
		password = request.data['password']

		user = User.objects.get(username = username, password = password)
		if user:
			try:
				payload = jwt_payload_handler(user)
				token = jwt.encode(payload, Settings.SECRET_KEY)
				user_details = {}
				user_details['name'] = "%s %s"%(user.first_name, user.last_name)
				user_details['token'] = token
				user_logged_in.send(sender=user.__class__,
									request=request, user=user)
				return Response(user_details, status=status.HTTP_201_CREATED)
			except Exception as e:
				raise e
		else:
			return Response({"error": "can not authenticate with given credenctials"}, status=status.HTTP_403_FORBIDDEN)
	except Exception as e:
		res = {'error': 'please provide a email and a password'}
		return Response(res)

def get_user_token(request):
	"""
	Custom Function to get user token
	"""

	jwt_payload_handler = Settings.JWT_PAYLOAD_HANDLER
	jwt_encode_handler = Settings.JWT_ENCODE_HANDLER

	payload = jwt_payload_handler(user = request.user)
	token = jwt_encode_handler(payload)
	return Response({"token": token,
					"success":True,
					})

def get_user_id_from_payload(request):
	return jwt_get_user_id_from_payload_handler(request.user)

# if you want to decode the token and verify any custom claims
def jwt_decode(token):
	options = {
		'verify_exp': Settings.JWT_VERIFY_EXPIRATION,
	}
	# get user from token, BEFORE verification, to get user secret key
	unverified_payload = jwt.decode(token, None, False)
	secret_key = jwt_get_secret_key(unverified_payload)
	return jwt.decode(
		token,
		Settings.JWT_PUBLIC_KEY or secret_key,
		Settings.JWT_VERIFY,
		issuer=Settings.JWT_ISSUER,
		algorithms=[Settings.JWT_ALGORITHM]
	)

# @login_required
# @allowed_users(allowed_roles = ["admin","teachers"])
# def get_teachers(request):
# 		return render(request, 'app/teachers.html')


