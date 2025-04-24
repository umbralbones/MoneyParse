from django.db import models
from django.conf import settings


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['date']),
        ]
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default='income')
    
    EXPENSE_CATEGORIES = (
        ('housing', 'Housing'),
        ('transportation', 'Transportation'),
        ('food', 'Food & Dining'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('education', 'Education'),
        ('savings', 'Savings'),
        ('other', 'Other'),
    )
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ${self.amount}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount <= 0:
            raise ValidationError('Amount must be positive')
        if self.transaction_type == 'expense' and not self.category:
            raise ValidationError('Category is required for expenses')
        if self.category and self.transaction_type != 'expense':
            self.category = None  # Clear category if not an expense
        if self.category == 'other' and not self.description:
            raise ValidationError('Description is required when category is Other')

