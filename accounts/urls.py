from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from index.models import *
from accounts.forms import UserLoginForm

app_name = 'account'


urlpatterns = [
    path('',views.index,name='index'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',authentication_form=UserLoginForm, redirect_authenticated_user=True, extra_context={'upcoming_game': str(0),}), name='login'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit', views.edit_profile,name='profile_edit'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangeView.as_view(success_url=reverse_lazy('account:logout'),template_name='account/password_change.html',extra_context={}), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('account:password_reset_done'),template_name='account/password_reset.html',
            extra_context={"post_change_redirect":"password_change_done"}),
            name='password_reset',
            ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html',
            extra_context={"post_change_redirect":"password_change_done"}), name='password_reset_done'),
    path('reset/<slug:uidb64>/<slug:token>/',
        auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_reset_complete'),template_name='account/set_password_form.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_completed.html'), name='password_reset_complete'),
]
