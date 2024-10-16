from django.urls import path, include
from . import views
from .views import verify_email
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile_update/', views.UserUpdateView.as_view(), name='profile_update'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done'),

    path('verification_page/', verify_email, name='verification_page'),
]