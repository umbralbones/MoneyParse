from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from decimal import Decimal
from .models import Budget, BudgetItem

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'description', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter budget name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01'
            })
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount or amount <= 0:
            raise ValidationError('Budget amount must be greater than zero.')
        return Decimal(str(amount))

class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = ['name', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item name'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01'
            })
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount or amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        return Decimal(str(amount))

class BaseBudgetItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if not self.forms:
            return

        valid_forms = [form for form in self.forms 
                      if form.cleaned_data and not form.cleaned_data.get('DELETE', False)]

        if not valid_forms:
            raise ValidationError('At least one budget item is required.')

        total = sum(form.cleaned_data.get('amount', 0) for form in valid_forms)
        budget_amount = self.instance.amount if self.instance.pk else \
                       self.data.get(f'{self.prefix}-0-amount', 0)

        try:
            budget_amount = Decimal(str(budget_amount))
            if total > budget_amount:
                raise ValidationError(
                    f'Total of items (${total:.2f}) exceeds budget amount (${budget_amount:.2f})'
                )
        except (TypeError, ValueError):
            raise ValidationError('Invalid budget amount.')

BudgetItemFormSet = inlineformset_factory(
    Budget,
    BudgetItem,
    form=BudgetItemForm,
    formset=BaseBudgetItemFormSet,
    fields=['name', 'amount'],
    extra=1,
    can_delete=True
)