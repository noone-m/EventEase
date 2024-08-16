from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TransactionSerializer, UserWalletSerializer

from django.db import transaction as db_transaction

from accounts.models import User
from accounts.permissions import IsAdminUser,DefaultOrIsAdminUser

from .models import UserWallet,Transaction


class RetrieveWalletAPIView(APIView):
    permission_classes = [IsAdminUser,]
    def get(self, request, user_id):
        user = get_object_or_404(User,id = user_id)
        wallet = UserWallet.objects.get(user=user)
        serializer = UserWalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RetrieveMyWalletAPIView(APIView):
    def get(self, request):
        wallet = UserWallet.objects.get(user=request.user)
        serializer = UserWalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CreditWalletView(APIView):
    def post(self, request):
        wallet = get_object_or_404(UserWallet,user = request.user)
        amount = request.data.get('amount')

        if not amount:
            return Response({'message':'amount is required'},status= status.HTTP_400_BAD_REQUEST)
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            wallet.add_funds(amount)
            return Response({'status': 'Credit successful'}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class DebitWalletView(APIView):
    def post(self, request, format=None):
        wallet = get_object_or_404(UserWallet,user = request.user)
        amount = request.data.get('amount')
        
        if not amount:
            return Response({'error': 'amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            wallet.withdraw_funds(amount)
            return Response({'status': 'Debit successful'}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class TransactionsAPIView(APIView):
    permission_classes = [DefaultOrIsAdminUser,]
    def get(self, request):
        if request.user.is_superuser:
            transactions = Transaction.objects.all()
        else:
            wallet = get_object_or_404(UserWallet,user = request.user)
            transactions = Transaction.objects.filter(Q(wallet=wallet) | Q(sender=wallet) | Q(receiver=wallet))
        serializer = TransactionSerializer(transactions,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
