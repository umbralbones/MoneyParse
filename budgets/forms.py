from django import forms
from .models import Budget, Item
from django.forms.models import inlineformset_factory


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'description', 'amount']

ItemFormSet = inlineformset_factory(
    Budget,
    Item,
    fields=['name', 'amount'],
    extra=1,            # how many blank items to show by default
    can_delete=True     # allow users to delete items
)