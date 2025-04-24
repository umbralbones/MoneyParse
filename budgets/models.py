from django.db import models
from django.conf import settings
from decimal import Decimal

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', '-created_at'])]

    def __str__(self):
        return self.name

    def get_total_items(self):
        if not hasattr(self, '_total_items'):
            self._total_items = self.items.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        return self._total_items

    def get_remaining_amount(self):
        return self.amount - self.get_total_items()

    def get_percentage_used(self):
        total = self.get_total_items()
        if not total or not self.amount:
            return Decimal('0.00')
        return min((total / self.amount) * 100, Decimal('100.00'))

class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name} (${self.amount})"