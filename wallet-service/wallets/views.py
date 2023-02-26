from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import WalletBalanceSerializer
from .models import NairaWallet
from .permissions import IsOwnerOrReadOnly

# Create your views here.


class RetrieveWalletBalance(generics.RetrieveAPIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    authentication_classes = []
    serializer_class = WalletBalanceSerializer
    queryset = NairaWallet.objects.all()

    def get_object(self):
        user = self.request.user
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj