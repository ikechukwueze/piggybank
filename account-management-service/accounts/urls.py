from django.urls import path
from knox import views as knox_views
from . import views



urlpatterns = [
    path("signup/", views.AccountSignUpView.as_view(), name="account_signup"),
    path("login/", views.AccountLoginView.as_view(), name="account_login"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_account_password"),
    path("logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]