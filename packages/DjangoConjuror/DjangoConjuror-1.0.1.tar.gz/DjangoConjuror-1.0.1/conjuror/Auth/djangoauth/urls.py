from django.urls import path
from djangoauth import views

app_name = 'auth'

urlpatterns = [
    path('', views.user_login, name="login"),  # This will map to /auth/
    path('login/', views.user_login, name="login"),  # This will map to /auth/login/
    path('signup/', views.signup, name="signup") , # This will map to /auth/signup/
    path('logout/', views.user_logout, name='logout'), # This will map to /auth/logout/
    path('reset_password/', views.login_reset_password, name='reset_password'), # This will map to /auth/rese_password/
    path('update_password/<str:reset_key>', views.update_password, name='update_password'), # This will map to /auth/rese_password/
    path('update_password_post/', views.update_password_post, name='update_password_post'), # This will map to /auth/rese_password/
    path('home/',views.home , name="home")
]
