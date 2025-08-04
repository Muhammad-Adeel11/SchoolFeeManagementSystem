from django.db import models
from accounts.models import CustomUser
# Create your models here.

class FeeStructure(models.Model):
    FEE_TYPES = (
        ('monthly', 'Monthly'),
        ('term', 'Term-wise'),
    )
    fee_type = models.CharField(max_length=10, choices=FEE_TYPES)
    amount = models.FloatField()
    due_date = models.DateField()
    def __str__(self):
        return f"{self.fee_type.capitalize()} - {self.amount} - Due: {self.due_date}"

class Payment(models.Model):
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount_paid = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50) # 'Stripe' or 'BankTransfer' etc
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)  # New Payment Stripe is Added
    def __str__(self):
        return f"{self.parent.email} - {self.amount_paid} USD"