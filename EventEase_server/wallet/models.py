from django.db import models
from django.db import transaction as db_transaction
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.conf import settings
from rest_framework.exceptions import ValidationError, PermissionDenied
from services.models import Reservation, Order

FEE_PERCENTAGE = 0.05

class Wallet(models.Model):
    """
    Model to represent a user's wallet.
    """
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        editable=False,
        default=0.0,
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username}'s wallet with balance {self.balance} {self.currency}"
    
    def add_funds(self, amount, order = None, reservation = None):
        with db_transaction.atomic():
            self.balance = float(self.balance) + amount
            self.save()
            Transaction.objects.create(wallet=self, amount=amount, transaction_type='credit', order = order, reservation = reservation)

    def withdraw_funds(self, amount, order = None, reservation = None):
        if self.balance >= amount:
            with db_transaction.atomic():
                self.balance = float(self.balance) - amount
                self.save()
                Transaction.objects.create(wallet=self,
                                            amount=-amount, 
                                            transaction_type='debit',
                                            order = order,
                                            reservation = reservation)
        else:
            raise ValidationError("Insufficient funds")

    def transfer_funds(self, target_wallet, amount, order=None, reservation=None):
        fee = amount * FEE_PERCENTAGE
        amount_plus_fee = amount + fee
        if self.balance >= amount_plus_fee:
            with db_transaction.atomic():
                self.withdraw_funds(amount_plus_fee, order=order, reservation=reservation)
                target_wallet.add_funds(amount_plus_fee, order=order, reservation=reservation)
                transaction = Transaction.objects.create(wallet=self,
                                            amount= -amount_plus_fee,
                                            transaction_type='transfer',
                                            fee = fee,
                                            sender = self,
                                            receiver = target_wallet,
                                            order = order,
                                            reservation = reservation
                                            )
        else:
            raise ValidationError("Insufficient funds")
    
class CenterWallet(Wallet):
    """
    Represents the system's central wallet for handling transactions and fees.
    """
    def transfer_funds(self, target_wallet, amount, order=None, reservation=None):
        if self.balance >= amount:
            with db_transaction.atomic():
                self.withdraw_funds(amount, order=order, reservation=reservation)
                target_wallet.add_funds(amount, order=order, reservation=reservation)
                transaction = Transaction.objects.create(wallet=self,
                                            amount= -amount,
                                            transaction_type='transfer',
                                            fee = 0,
                                            sender = self,
                                            receiver = target_wallet,
                                            order = order,
                                            reservation = reservation
                                            )
        else:
            raise ValidationError("Insufficient funds")
  

class UserWallet(Wallet):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
        

TRANSACTION_TYPE_CHOICES = [
    ('credit', 'Credit'),
    ('debit', 'Debit'),
    ('transfer', 'Transfer'),
]

class Transaction(models.Model):
    """
    Model to represent a single transaction affecting a wallet.
    """
    reservation = models.ForeignKey(Reservation,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null =True)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name='sent_transactions')
    receiver = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name='received_transactions')
    fee = models.DecimalField(max_digits=20, decimal_places=2, null = True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE_CHOICES)
    made_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Prevent saving if the record is not new
        if self.pk is not None:
            raise PermissionDenied("Modification of existing transactions is not allowed.")
        super(Transaction, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise PermissionDenied("Deletion of transactions is not allowed.")
    def __str__(self):
        return f"{self.transaction_type} of {self.amount} SYP on {self.made_at}"


