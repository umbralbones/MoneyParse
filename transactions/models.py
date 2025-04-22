from django.db import models
from django.conf import settings


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=255, default='No description')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default='income')

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ${self.amount}"