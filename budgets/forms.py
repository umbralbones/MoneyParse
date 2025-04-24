from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Budget, BudgetItem

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional description'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter budget name'}),
            'amount': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01', 'placeholder': '0.00'})
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError('Budget amount must be greater than zero.')
        return amount

class BaseBudgetItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        valid_forms = [form for form in self.forms 
                       if form.cleaned_data and not form.cleaned_data.get('DELETE', False)]

        if not valid_forms:
            raise ValidationError('At least one budget item is required.')

        total = sum(form.cleaned_data.get('amount', 0) for form in valid_forms)
        budget_amount = self.instance.amount if self.instance and self.instance.amount else Decimal('0.00')

        if budget_amount > 0 and total > budget_amount:
            raise ValidationError(
                f'Total of items (${total:.2f}) exceeds budget amount (${budget_amount:.2f})'
            )

BudgetItemFormSet = inlineformset_factory(
    Budget,
    BudgetItem,
    formset=BaseBudgetItemFormSet,
    fields=['name', 'amount'],
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True,
    widgets={
        'name': forms.TextInput(attrs={'placeholder': 'Item name', 'class': 'form-control'}),
        'amount': forms.NumberInput(attrs={
            'min': '0.01',
            'step': '0.01',
            'placeholder': '0.00',
            'class': 'form-control'
        })
    }
)