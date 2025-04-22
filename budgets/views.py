# budgets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget
from .forms import BudgetForm, ItemFormSet
from django.contrib.auth.decorators import login_required



@login_required
def budgets(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'budgets/budgets.html', {'budgets': budgets})
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            # we need to save the Budget first so the formset can attach to it
            budget = form.save()
            formset = ItemFormSet(request.POST, instance=budget)
            if formset.is_valid():
                formset.save()
                return redirect('budget_detail', pk=budget.pk)
        else:
            # if the Budget form failed, still bind the formset so errors show
            formset = ItemFormSet(request.POST)
    else:
        form = BudgetForm()
        # pass an empty “unsaved” Budget instance to generate blank item forms
        formset = ItemFormSet(instance=Budget())

    return render(request, 'budgets/budget_form.html', {
        'form': form,
        'formset': formset,
    })


def budget_edit(request, pk):
    budget  = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        form     = BudgetForm(request.POST, instance=budget)
        formset  = ItemFormSet(request.POST, instance=budget)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('budget_detail', pk=budget.pk)
    else:
        form     = BudgetForm(instance=budget)
        formset  = ItemFormSet(instance=budget)

    return render(request, 'budgets/budget_form.html', {
        'form': form,
        'formset': formset,
    })



def budget_detail(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    # budget.items will be the related Items via related_name='items'
    return render(request, 'budgets/budget_detail.html', {
        'budget': budget
    })

