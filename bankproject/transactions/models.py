from django.db import models
from accounts.models import Account
from django.contrib.auth.models import User
import uuid

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.custom_name} by {str(self.user)}"

class ScheduledPayment(models.Model):
    from_account = models.ForeignKey(Account, related_name='scheduled_payments_from', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='scheduled_payments_to', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.amount)} to {str(self.to_account)} on {str(self.payment_date)}"

class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_receipts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_receipts')
    date_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"Receipt {self.id}: {self.sender.get_full_name()} to {self.recipient.account_number}"

    @property
    def sender_name(self):
        return f"{self.sender.first_name} {self.sender.last_name}"

    @property
    def recipient_details(self):
        return f"{self.recipient.user.first_name} {self.recipient.user.last_name} - {self.recipient.account_number}"



class PendingTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account_id = models.IntegerField()
    to_account_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_now = models.BooleanField()
    payment_date = models.DateTimeField(null=True, blank=True)
    save_beneficiary = models.BooleanField()
    beneficiary_name = models.CharField(max_length=255, blank=True)
    receipt_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pending Transaction for {self.user.username}"
