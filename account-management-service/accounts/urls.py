from django.urls import path
from knox import views as knox_views
from . import views



urlpatterns = [
    path("signup/", views.AccountSignUpView.as_view(), name="account_signup"),
    path("login/", views.AccountLoginView.as_view(), name="account_login"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_account_password"),
    path("forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"),
    path("password-reset/<encoded-account-id>/<passoword-reset-token>/", views.EmailPasswordResetWithToken.as_view(), name='email-password-reset'),
    path("update-bvn/", views.UpdateBvnView.as_view(), name="update_bvn"),
    path("logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]