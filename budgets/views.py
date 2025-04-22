# budgets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget
from .forms import BudgetForm, ItemFormSet
from django.contrib.auth.decorators import login_required



@login_required
def budgets(request):
    qs = Budget.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'budgets/budgets.html', {'budgets': qs})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form    = BudgetForm(request.POST)
        formset = ItemFormSet(request.POST)                # bind your items, too

        if form.is_valid() and formset.is_valid():
            # don’t save to DB yet — we need to attach the user
            budget      = form.save(commit=False)
            budget.user = request.user                      # ← set the owner
            budget.save()

            # now attach the items to that saved budget
            formset.instance = budget
            formset.save()

            return redirect('budgets')  # or whatever your list‑view name is

    else:
        form    = BudgetForm()
        # pass in an “unsaved” Budget so empty_form works
        formset = ItemFormSet(instance=Budget(user=request.user))

    return render(request, 'budgets/budget_form.html', {
        'form':    form,
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

