import constants
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import os
from django.contrib.auth import get_user_model
from decimal import *
import random
import string
import os
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings 


User = get_user_model()

def get_case_insensitive_user(email):
	"""
	Get User based on email case insensitive.
	"""
	try:
		user = User.objects.get(email__iexact = email)
	except MultipleObjectsReturned:
		try:
			user = User.objects.get(email = email.lower())
		except:
			try:
				user = User.objects.filter(email__iexact = email).order_by('-dt_timestamp')[0]
			except:
				return None
	except:
		return None
	
	return user

chars = string.ascii_letters + string.digits
pwdSize = 12

def generate_random_password_key(length = None):
	"""
	Generate Password Reset Key .
	"""
	if length:
		try:
			length = int(length)
		except:
			length = pwdSize
	else:
		length = pwdSize

	temp_code = ''.join((random.choice(chars)) for x in range(length))
	unique = False
	while not unique:
		try:
			User.objects.get(password_reset_key = temp_code)
		except ObjectDoesNotExist:
			unique = True
			break
		except MultipleObjectsReturned:
			temp_code = ''.join((random.choice(chars)) for x in range(length))
			continue
		else:
			temp_code = ''.join((random.choice(chars)) for x in range(length))
			continue

	return temp_code


def reset_password_email(request, email, user_uuid, password_reset_key):
	"""
	Send Email For Passwrod Reset.
	"""
	url = constants.SITE_MARKETING_URL + '/auth' +'/update_password/{}'.format(password_reset_key)
	subject = 'Reset Password for ' + constants.SITE_URL
	context = {
        'user_email': email,
        'reset_url': url,
        'site_name': constants.SITE_URL,  
    }
	html_content = render_to_string(os.path.join(settings.BASE_DIR , 'djangoauth','email_templates/password_reset_email.html'), context)
	try:
		email =	send_mail(subject, '', settings.EMAIL_HOST, [email], html_message=html_content)
		return True  
	except Exception as e:
		print(e)
		return False 