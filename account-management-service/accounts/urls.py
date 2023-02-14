from django.urls import path
from knox import views as knox_views
from . import views



urlpatterns = [
    path("signup/", views.AccountSignUpView.as_view(), name="account_signup"),
    path("login/", views.AccountLoginView.as_view(), name="account_login"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_account_password"),
    path("request-password-reset/<encrypted_user_id>/<password_reset_token>/", views.RequestPasswordResetView.as_view(), name="request-password-reset"),
    path("password-reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path("update-bvn/", views.UpdateBvnView.as_view(), name="update_bvn"),
    path("logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]