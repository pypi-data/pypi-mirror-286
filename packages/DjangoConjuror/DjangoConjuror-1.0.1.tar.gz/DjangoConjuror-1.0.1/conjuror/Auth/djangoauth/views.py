from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.shortcuts import redirect
from djangoauth import common
import datetime
from django.utils import timezone

## Loading Custom User Model
User = get_user_model()


    
@login_required(login_url='login')
def home(request):
    """
    Simple Home Page View
    """
    context = {
        'user_email': request.user.email,
    }
    return render(request, 'auth/index.html', context)

def user_login(request):
    """
    Login a User.
    
    """
    if request.user.is_authenticated:
        messages.error(request, 'User is already logged in !')
        return render(request, 'auth/index.html')
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, username=email, password=password, backend='django.contrib.auth.backends.ModelBackend')
            
            if user is not None:
                login(request, user)
                return redirect('auth:home')
            else:
                messages.error(request, "Invalid email or password.")
        
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
    
    return render(request, 'auth/login.html')



def signup(request):
    """
    Creates a User.
    
    """
    if request.user.is_authenticated:
        messages.error(request, 'User is already logged in !')
        return render(request, 'auth/index.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return render(request, 'auth/signup.html')

        try:
            user = User.objects.create(full_name=name, email=email, password=make_password(password))
            messages.success(request, 'Your account was successfully created.')
            return redirect('auth:login')
        except Exception as e:
            messages.error(request, 'There was an error creating your account. Please try again.')

        return redirect('auth:signup')
    else:
        return render(request, 'auth/signup.html')



def user_logout(request):
    """
    Logout a User.
    
    """
    logout(request)
    return redirect('auth:login')

def login_reset_password(request):
    """
    It will send an email to reset your password. The Reset Link will Expires after 1 day.
    
    """
    if request.user.is_authenticated:
        messages.error(request, 'User is already logged in !')
        return render(request, 'auth/index.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        user = common.get_case_insensitive_user(request.POST.get('email'))
        if not user:
            messages.error(request, 'We could not find an account with that email')
            return render(request, 'auth/forget_password.html')
        user.password_reset_key = common.generate_random_password_key(length = 25)
        user.password_reset_date = timezone.now()
        user.save()
        if common.reset_password_email(request , user.email, user.id, user.password_reset_key):
            messages.success(request, 'Password reset email sent')
            return redirect('auth:login')  
        else:
            messages.error(request, 'Failed to send reset password email')
            return redirect('auth:reset_password')  


    return render(request, 'auth/forget_password.html')


def update_password(request, reset_key):
    """
    It will Check that the Reset Password link is not expired.
    
    """
    if request.method == 'GET':
        user_model = get_user_model()
        user = user_model.objects.filter(password_reset_key=reset_key).first()

        if not user:
            messages.error(request, 'Invalid reset password link.')
            return redirect('auth:login')

        reset_time_limit = datetime.timedelta(hours=1)
        if timezone.now() > user.password_reset_date + reset_time_limit:
            messages.error(request, 'Reset password link has expired. Please request a new one.')
            return redirect('auth:reset_password')
        context = {
            'reset_key': reset_key
        }
        return render(request, 'auth/update_password.html', context)

    return render(request, 'auth/login.html')




def update_password_post(request):
    """
    It willl Update Passowrd.
    """
    if request.method == 'POST':
        reset_key = request.POST.get('reset_key')
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')


        user_model = get_user_model()
        user = user_model.objects.filter(password_reset_key=reset_key).first()

        if not user:
            messages.error(request, 'Invalid reset password link.')
            return redirect('auth:login')

        reset_time_limit = datetime.timedelta(hours=1)
        if timezone.now() > user.password_reset_date + reset_time_limit:
            messages.error(request, 'Reset password link has expired. Please request a new one.')
            return redirect('auth:reset_password')
        
        if password != confirm_password:
            messages.error(request, 'Password is not same!')
            return redirect('auth:update_password')

        # Update the user's password
        user.set_password(password)
        user.password_reset_key = None
        user.password_reset_date = None
        user.save()

        messages.success(request, 'Password has been successfully reset. You can now log in with your new password.')
        return redirect('auth:login')

    return render(request, 'auth/login.html')
