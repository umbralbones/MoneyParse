# budgets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Budget, Item
from .forms import BudgetForm, ItemFormSet
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


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


@login_required
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        formset = ItemFormSet(request.POST, instance=budget)
        if form.is_valid() and formset.is_valid():
            budget = form.save()
            formset.save()
            return redirect('budget_detail', pk=budget.pk)
    else:
        form = BudgetForm(instance=budget)
        formset = ItemFormSet(instance=budget)

    return render(request, 'budgets/budget_form.html', {
        'form': form,
        'formset': formset,
        'budget': budget
    })



def budget_detail(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    # budget.items will be the related Items via related_name='items'
    return render(request, 'budgets/budget_detail.html', {
        'budget': budget
    })

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budgets')
    return render(request, 'budgets/confirm_delete.html', {
        'budget': budget
    })

@login_required
@require_POST
def item_delete(request, budget_pk, item_pk):
    budget = get_object_or_404(Budget, pk=budget_pk, user=request.user)
    item = get_object_or_404(Item, pk=item_pk, budget=budget)
    item.delete()
    return JsonResponse({'status': 'success'})
