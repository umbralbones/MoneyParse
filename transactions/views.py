from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from django.utils.timezone import now
from .models import MonthlyBudget
from .forms import TransactionForm
from .forms import MonthlyBudgetForm
from django.contrib.auth.decorators import login_required

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')

    return render(request, 'transactions/confirm_delete.html', {'transaction': transaction})

@login_required
def monthly_budget(request):
    if request.method == 'POST':
        form = MonthlyBudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('monthly_budget')
    else:
        form = MonthlyBudgetForm()
    return render(request, 'transactions/monthly_budget.html', {'form': form})

@login_required
def set_budget(request):
    today = now()
    month_start = today.replace(day=1)
    budget, created = MonthlyBudget.objects.get_or_create(user=request.user, month=month_start)

    if request.method == 'POST':
        form = MonthlyBudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MonthlyBudgetForm(instance=budget)

    return render(request, 'transactions/set_budget.html', {'form': form})