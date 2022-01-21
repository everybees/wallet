from django.contrib import admin

from accounts.models import Transaction, User, Wallet

# Register your models here.

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Transaction)
