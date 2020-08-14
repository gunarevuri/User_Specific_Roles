 
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group, Permission, GroupManager,Group
from .validators import UnicodeUsernameValidator


standard_list = [1,2,3,4,5,6,7,8,9,10]

def update_last_login(sender, user, **kwargs):
	"""
	A signal receiver which updates the last_login date for
	the user logging in.
	"""
	user.last_login = timezone.now()
	user.save(update_fields=['last_login'])


class PermissionManager(models.Manager):
	use_in_migrations = True

	def get_by_natural_key(self, codename, app_label, model):
		return self.get(
			codename=codename,
			content_type=ContentType.objects.db_manager(self.db).get_by_natural_key(app_label, model),
		)

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		if not username:
			raise ValueError('The given username must be set')
		email = self.normalize_email(email)
		# Lookup the real model class from the global app registry so this
		# manager method can be used in migrations. This is fine because
		# managers are by definition working on the real model.
		GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
		username = GlobalUserModel.normalize_username(username)
		user = self.model(username=username, email=email, **extra_fields)
		user.password = make_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_student', True)
		extra_fields.setdefault('is_teacher',True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		if extra_fields.get('is_student') is not True:
			raise ValueError('Superuser must have is_student=True.') 
		if extra_fields.get('is_teacher') is not True:
			raise ValueError('Superuser must have is_teacher=True.') 
			

		return self._create_user(username, email, password, **extra_fields)

	def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
		if backend is None:
			backends = auth._get_backends(return_tuples=True)
			if len(backends) == 1:
				backend, _ = backends[0]
			else:
				raise ValueError(
					'You have multiple authentication backends configured and '
					'therefore must provide the `backend` argument.'
				)
		elif not isinstance(backend, str):
			raise TypeError(
				'backend must be a dotted import path string (got %r).'
				% backend
			)
		else:
			backend = auth.load_backend(backend)
		if hasattr(backend, 'with_perm'):
			return backend.with_perm(
				perm,
				is_active=is_active,
				include_superusers=include_superusers,
				obj=obj,
			)
		return self.none()



class User(AbstractBaseUser, PermissionsMixin):
	"""
	An abstract base class implementing a fully featured User model with
	admin-compliant permissions.
	Username and password are required. Other fields are optional.
	"""
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
		_('username'),
		max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)
	first_name = models.CharField(_('first name'), max_length=150, blank=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True)
	email = models.EmailField(_('email address'), blank=True)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	is_student = models.BooleanField(default=True)
	is_teacher = models.BooleanField(default=False)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		swappable = 'AUTH_USER_MODEL'

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def get_full_name(self):
		"""
		Return the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		"""Return the short name for the user."""
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""Send an email to this user."""
		send_mail(subject, message, from_email, [self.email], **kwargs)

class Student(models.Model):
	" Student Model creation"
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	standard = models.IntegerField(choices=[(x,x) for x in standard_list])
	address = models.CharField(max_length=500)
	favourite_subject = models.CharField(max_length=100)


class Teacher(models.Model):
	" Teacher Model Creation "
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	address = models.CharField(max_length= 255)
	favourite_subject = models.CharField(max_length=255)

















