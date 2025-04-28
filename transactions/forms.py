from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'amount', 'transaction_type', 'category']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['category'].required = False

        self.fields['category'].choices = [(None, '---------')] + list(Transaction.EXPENSE_CATEGORIES)

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        description = cleaned_data.get('description')

        if transaction_type == 'expense':
            if not category:
                self.add_error('category', 'Category is required for expenses')
            elif category == 'other' and not description:
                self.add_error('description', 'Description is required when category is Other')
        elif category:
            cleaned_data['category'] = None

        return cleaned_data
