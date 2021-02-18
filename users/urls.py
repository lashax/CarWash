from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as users_view


urlpatterns = [
    path('profile/', users_view.profile, name='profile'),
    path('register/', users_view.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password/password-reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password/password-reset-done.html'),
         name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password/password-reset-complete.html'),
         name='password_reset_complete')
]
