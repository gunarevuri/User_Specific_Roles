from rest_framework import serializers

from .models import User, Student, Teacher

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["username", "firstname", "email", "is_student", "is_teacher"]

class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = '__all__'
		

