from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Budget, BudgetItem
from .forms import BudgetForm, BudgetItemFormSet

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            formset = BudgetItemFormSet(request.POST, instance=budget)

            if formset.is_valid():
                with transaction.atomic():
                    budget.save()
                    formset.save()
                    messages.success(request, 'Budget created successfully!')
                    return redirect('budget_detail', pk=budget.pk)
            else:
                messages.error(request, 'Please correct the errors in your budget items.')
        else:
            formset = BudgetItemFormSet(request.POST)
    else:
        form = BudgetForm()
        formset = BudgetItemFormSet()

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
        formset = BudgetItemFormSet(request.POST, instance=budget)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
                messages.success(request, 'Budget updated successfully!')
                return redirect('budget_detail', pk=budget.pk)
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = BudgetForm(instance=budget)
        formset = BudgetItemFormSet(instance=budget)

    return render(request, 'budgets/budget_form.html', {
        'form': form,
        'formset': formset,
        'budget': budget,
        'title': 'Edit Budget'
    })

@login_required
def budget_detail(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    budget.refresh_from_db()
    total_items = budget.get_total_items()
    remaining = budget.get_remaining_amount()

    return render(request, 'budgets/budget_detail.html', {
        'budget': budget,
        'total_items': total_items,
        'remaining': remaining
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
@require_POST
def budget_item_delete(request, budget_pk, item_pk):
    budget = get_object_or_404(Budget, pk=budget_pk, user=request.user)
    item = get_object_or_404(BudgetItem, pk=item_pk, budget=budget)
    item.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Item deleted successfully',
        'total_items': float(budget.get_total_items()),
        'remaining': float(budget.get_remaining_amount())
    })