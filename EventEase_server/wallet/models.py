from django.db import models
from django.db import transaction as db_transaction
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from django.core.exceptions import PermissionDenied
from django.conf import settings

class Wallet(models.Model):
    """
    Model to represent a user's wallet.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        validators=[MinValueValidator(0.0)],
        editable=False,
    ) # this field should be encrypted
    currency = models.CharField(max_length=3)  # ISO 4217 currency codes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username}'s wallet with balance {self.balance} {self.currency}"
    
    def add_funds(self, amount):
        with db_transaction.atomic():
            self.balance += amount
            self.save()
            Transaction.objects.create(wallet=self, amount=amount, transaction_type='credit')

    def withdraw_funds(self, amount):
        if self.balance >= amount:
            with db_transaction.atomic():
                self.balance -= amount
                self.save()
                Transaction.objects.create(wallet=self, amount=-amount, transaction_type='debit')
        else:
            raise ValueError("Insufficient funds")

    def transfer_funds(self, target_wallet, amount):
        if self.balance >= amount:
            with db_transaction.atomic():
                self.withdraw_funds(amount)
                target_wallet.add_funds(amount)
        else:
            raise ValueError("Insufficient funds")
        

class Transaction(models.Model):
    """
    Model to represent a single transaction affecting a wallet.
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_type = models.CharField(max_length=10)  # 'credit' or 'debit'
    timestamp = models.DateTimeField(default=now)
    made_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Prevent saving if the record is not new
        if self.pk is not None:
            raise PermissionDenied("Modification of existing transactions is not allowed.")
        super(Transaction, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise PermissionDenied("Deletion of transactions is not allowed.")
    def __str__(self):
        return f"{self.transaction_type} of {self.amount} {self.wallet.currency} on {self.timestamp}"
