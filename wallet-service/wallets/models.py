from django.db import models
from uuid import uuid4

# Create your models here.


class Account(models.Model):
    id = models.UUIDField(primary_key=True)



class Wallet(models.Model):
    class WalletStatus(models.TextChoices):
        active = 'ACTIVE', 'ACTIVE'
        inactive = 'INACTIVE', 'INACTIVE'
        pnd = 'PND', 'PND'

    id = models.UUIDField(primary_key=True, default=uuid4)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=11, decimal_places=2)
    status = models.CharField(choices=WalletStatus.choices, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NairaWallet(Wallet):
    currency = models.CharField(choices=[('NGN', 'NGN')], default='NGN', max_length=3)

    def __str__(self) -> str:
        return str(self.owner)