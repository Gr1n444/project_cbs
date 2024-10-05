from django.urls import path
from app_users.views import *


urlpatterns = [
    path('', landing, name='landing'),
    path('login/', loginUser, name='login'),
    path('register/', registerUser, name='register'),
    path('logoutUser/', logoutUser, name='logoutUser'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView, name='confirm_email'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user-profile/<str:username>/', userProfile, name='user-profile'),
    path('account/', userAccount, name='account'),
    path('edit-account/', editUserAccount, name='edit-account'),
    path('leaderboard/', leaderboardUsers, name='leaderboardUsers'),
    path('leaderboard_event/', leaderboardEvent, name='leaderboardEvent'),
    
]