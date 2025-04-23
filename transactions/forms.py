from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
<<<<<<< HEAD
        fields = ['date', 'description', 'amount', 'transaction_type']
=======
        fields = ['date', 'description', 'amount', 'transaction_type']
>>>>>>> eec4dd1 (added budget page)
