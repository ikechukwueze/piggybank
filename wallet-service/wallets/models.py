from django.db import models
from uuid import uuid4

# Create your models here.

class WalletCurrency(models.Model):
    currency = models.CharField(max_length=50)
    currency_iso = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.currency_iso