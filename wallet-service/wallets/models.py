from django.db import models
from uuid import uuid4

# Create your models here.

class WalletCurrency(models.Model):
    currency = models.CharField(max_length=50)
    currency_iso = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.currency_iso


class Wallet(models.Model):
    class WalletStatus(models.TextChoices):
        active = 'ACTIVE', 'ACTIVE'
        inactive = 'INACTIVE', 'INACTIVE'
        pnd = 'PND', 'PND'

    id = models.UUIDField(primary_key=True, default=uuid4)
    owner = models.UUIDField()
    currency = models.ForeignKey(WalletCurrency, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(max_digits=11, decimal_places=2)
    status = models.CharField(choices=WalletStatus.choices, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.owner)