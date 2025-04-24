from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from .models import Budget, BudgetItem
from .forms import BudgetForm, BudgetItemFormSet

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)\
        .prefetch_related('items')\
        .annotate(total_items=Sum('items__amount'))\
        .order_by('-created_at')
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            formset = BudgetItemFormSet(request.POST, instance=budget, prefix='items')
            
            if formset.is_valid():
                try:
                    with transaction.atomic():
                        budget.save()
                        formset.save()
                        messages.success(request, 'Budget created successfully!')
                        return redirect('budget_detail', pk=budget.pk)
                except Exception as e:
                    messages.error(request, str(e))
            else:
                for error in formset.non_form_errors():
                    messages.error(request, error)
        else:
            formset = BudgetItemFormSet(request.POST, prefix='items')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BudgetForm()
        formset = BudgetItemFormSet(prefix='items')

    return render(request, 'budgets/budget_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Budget'
    })

@login_required
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        formset = BudgetItemFormSet(request.POST, instance=budget, prefix='items')
        
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    formset.save()
                    messages.success(request, 'Budget updated successfully!')
                    return redirect('budget_detail', pk=budget.pk)
            except Exception as e:
                messages.error(request, str(e))
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    messages.error(request, error)
    else:
        form = BudgetForm(instance=budget)
        formset = BudgetItemFormSet(instance=budget, prefix='items')

    return render(request, 'budgets/budget_form.html', {
        'form': form,
        'formset': formset,
        'budget': budget,
        'title': 'Edit Budget'
    })

@login_required
def budget_detail(request, pk):
    budget = get_object_or_404(
        Budget.objects.prefetch_related('items'),
        pk=pk,
        user=request.user
    )
    total_items = budget.get_total_items()
    remaining = budget.get_remaining_amount()
    percentage = budget.get_percentage_used()
    
    return render(request, 'budgets/budget_detail.html', {
        'budget': budget,
        'total_items': total_items,
        'remaining': remaining,
        'percentage': percentage
    })

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('budget_list')
    return render(request, 'budgets/budget_confirm_delete.html', {'budget': budget})

@login_required
def budget_item_delete(request, budget_pk, item_pk):
    budget = get_object_or_404(Budget, pk=budget_pk, user=request.user)
    item = get_object_or_404(budget.items, pk=item_pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Budget item deleted successfully!')
        return redirect('budget_detail', pk=budget_pk)
    return render(request, 'budgets/item_confirm_delete.html', {
        'budget': budget,
        'item': item
    })
