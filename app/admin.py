from django.contrib import admin

# Register your models here.

from app.models import User

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)

