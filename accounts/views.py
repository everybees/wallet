from django.shortcuts import render
from django.utils.datetime_safe import datetime
from rest_framework import viewsets
import string
import random

from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from accounts.models import User, Wallet, Transaction, TRANSACTION_TYPE

from permissions import IsAdmin, IsElite, IsNoob
from rest_framework.permissions import IsAuthenticated


def hello_world(request):
    return render(request, "hello_world.html")


def hello_jerry(request):
    return render(request, "hello_jerry.html")


def generate_wallet_id():
    S = 10
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    wallets = Wallet.objects.all().values_list('wallet_id', flat=True)
    while str(ran) in wallets:
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    return str(ran)


class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        user = serializer.save()
        Wallet.objects.create(
            user=user, wallet_id=generate_wallet_id(), is_default=True,
            currency=request.data.get('currency', 'NGN'),
        )

        return Response(serializer.data, status=201)

    # IsAuthenticated works for users that are logged in
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)


class WithdrawViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def withdraw(self, request):
        amount = request.data.get('amount')
        wallet_id = request.data.get('id')
        wallet = Wallet.objects.get(wallet_id=wallet_id)
        wallet.balance = wallet.balance - amount
        Wallet.objects.update(wallet)

        Transaction.objects.create(
            Transaction(wallet=wallet, amount=amount, transaction_type=TRANSACTION_TYPE('withdrawal'),
                        date_created=datetime.now()))
        return Response({"message": 'you have successfully withdrawn'}, amount)


class WalletViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def create_wallet(self, request):
        return Response({"message": "Wallet created successfully"}, status=200)
