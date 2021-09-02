"""Accounts URL Configuration"""

from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as accounts_auth

from accounts import views
from accounts.forms import ChangePasswordForm

app_name = 'accounts'

urlpatterns = [
    path('login/', accounts_auth.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', accounts_auth.LogoutView.as_view(),  name='logout'),
    path('list/', login_required(views.ProfileList.as_view()), name='list'),
    path('create/', login_required(views.ProfileCreate.as_view()), name='create'),
    path('<int:pk>/delete/', login_required(views.ProfileDelete.as_view()), name='delete'),
    path('<int:pk>/update/', login_required(views.ProfileUpdate.as_view()), name='update'),
    path('password-change/', accounts_auth.PasswordChangeView.as_view(
      success_url=reverse_lazy('accounts:password_change_done'),
      template_name='accounts/change_password.html',
      form_class=ChangePasswordForm
    ), name='password_change'),
    path('password-change/done/', accounts_auth.PasswordChangeDoneView.as_view(
      template_name='accounts/change_password_done.html'
    ), name='password_change_done')
]
