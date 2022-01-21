from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


USER_TYPE = (
    ('noob', 'Noob'),
    ('elite', 'Elite'),
    ('admin', 'Admin'),
)

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50, default="my_password")
    user_type = models.CharField(max_length=6, choices=USER_TYPE, default='noob')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_id = models.CharField(max_length=10, unique=True)
    is_default = models.BooleanField(default=False)
    currency = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.wallet_id


TRANSACTION_TYPE = (
    ('withdrawal', 'Withdrawal'),
    ('funding', 'Funding'),
)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField(max_length=10, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction_id
