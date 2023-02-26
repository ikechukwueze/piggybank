from django.urls import path
from . import views

urlpatterns = [
    path("balance/", views.RetrieveWalletBalance.as_view(), name="wallet_balance")
]
