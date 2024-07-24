from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.validators import validate_email


class UserManager(BaseUserManager):
	def create_user(self, email=None, password=None, firstname=None, lastname=None, age=None, gender=None, name=None, username=None, signup=None , **other_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		try:
			validate_email(email)
		except:
			raise ValueError('Users must have a valid email address')
		else:
			email = self.normalize_email(email)

		if signup:
			password_number = any(char.isdigit() for char in password)
			if not password_number:
				raise ValueError('Password must contain a number')

			password_length = True if len(password) > 6 else False
			if not password_length:
				raise ValueError('Password must be at least 6 characters')

			password_uppercase = (any(char.isupper() for char in password))

			if password_uppercase:
				raise ValueError('Password must contain an uppercase character')
			else:
				pass

		user = self.model(
			email = email,
			full_name = name,
			**other_fields
			)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password, **other_fields):
		"""
		Creates and saves a superuser with the given email and password.
		"""
		user = self.create_user(email = email, password=password, **other_fields)
		user.is_superuser = True
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	"""
	Custom User Model
	"""
	username = None
	dt_timestamp = models.DateTimeField(auto_now_add = True)
	last_login = models.DateTimeField(null = True, blank = True)
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
	full_name = models.CharField(max_length = 500, null = True, blank = True)
	first_name = models.CharField(max_length = 500, null = True, blank = True)
	middle_name = models.CharField(max_length = 150, null = True, blank = True)
	last_name = models.CharField(max_length = 500, null = True, blank = True)
	age = models.IntegerField(null = True, blank = True)
	gender = models.CharField(max_length = 200,choices = (('Male', 'Male'),('Female', 'Female'),('Other', 'Other')))
	address1 = models.CharField(max_length = 150, null = True, blank = True)
	address2 = models.CharField(max_length = 150, null = True, blank = True)
	city = models.CharField(max_length = 150, null = True, blank = True)
	state = models.CharField(max_length = 150, null = True, blank = True)
	zip = models.CharField(max_length = 5, null = True, blank = True)
	county = models.CharField(max_length = 250, null = True, blank = True)
	phone = models.CharField(max_length = 50, null = True, blank = True)
	photo_file = models.CharField(max_length = 300, null = True, blank = True)
	role = models.IntegerField(default=0)
	password_reset_key = models.CharField(max_length = 300, null = True, blank = True)
	password_reset_date = models.DateTimeField(null = True, blank = True)
	date_joined = models.DateTimeField(auto_now_add = True)

	timezone = models.CharField(
			max_length = 200,
			default = 'America/Chicago',
			choices = (
				('America/New_York', 'America/New_York'),
				('America/Detroit', 'America/Detroit'),
				('America/Kentucky/Louisville', 'America/Kentucky/Louisville'),
				('America/Kentucky/Monticello', 'America/Kentucky/Monticello'),
				('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'),
				('America/Indiana/Vincennes', 'America/Indiana/Vincennes'),
				('America/Indiana/Winamac', 'America/Indiana/Winamac'),
				('America/Indiana/Marengo', 'America/Indiana/Marengo'),
				('America/Indiana/Petersburg', 'America/Indiana/Petersburg'),
				('America/Indiana/Vevay', 'America/Indiana/Vevay'),
				('America/Chicago', 'America/Chicago'),
				('America/Indiana/Tell_City', 'America/Indiana/Tell_City'),
				('America/Indiana/Knox', 'America/Indiana/Knox'),
				('America/Menominee', 'America/Menominee'),
				('America/North_Dakota/Center', 'America/North_Dakota/Center'),
				('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'),
				('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'),
				('America/Denver', 'America/Denver'),
				('America/Boise', 'America/Boise'),
				('America/Phoenix', 'America/Phoenix'),
				('America/Los_Angeles', 'America/Los_Angeles'),
				('America/Metlakatla', 'America/Metlakatla'),
				('America/Anchorage', 'America/Anchorage'),
				('America/Juneau', 'America/Juneau'),
				('America/Sitka', 'America/Sitka'),
				('America/Yakutat', 'America/Yakutat'),
				('America/Nome', 'America/Nome'),
				('America/Adak', 'America/Adak'),
				('Pacific/Honolulu', 'Pacific/Honolulu'))
			)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()









