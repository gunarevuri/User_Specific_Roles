from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group

# Decorator function takes fun as arg or parameter add functionality before returning actual funcion
# view_func login page here 
# wrapper func executed first
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles = []):
	def decorator(view_func):
		def wrapper_function(request, *args, **kwargs):


			# print('working:', allowed_roles)
			group = None
			print(request.user.groups.all())
			l = list(request.user.groups.all())
			if len(l)>0:
				# li = request.user.groups.all()
				# for i in li:
				# 	print(i.name)
				# group = request.user.groups.all()[0].name
				# print(group)

				if "students" in allowed_roles and request.user.groups.filter(name = "students"):
					return view_func(request, *args, **kwargs)

				elif "teachers" in allowed_roles and request.user.groups.filter(name = "teachers"):
					return view_func(request, *args, **kwargs)

				elif "admin" in allowed_roles and request.user.groups.filter(name= "admin"):
					return view_func(request, *args, **kwargs)
				else:
					return HttpResponse("you are not authorized")
				# for role in allowed_roles:
				# 	if request.user.groups.filter(name = role):
				# 		return view_func(request, *args, **kwargs)
				# 	else:
				# 		return HttpResponse("you are not authorized")

			# if group in allowed_roles:
			# 	return view_func(request, *args, **kwargs)
			else:
				return HttpResponse("you are no authorized")
		return wrapper_function
	return decorator


# best only when a user have one been in one group
def admin_only_decoratory(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'students':
			return redirect('home')

		if group == 'teachers':
			return redirect('home')

	return wrapper_func


