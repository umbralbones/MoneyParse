from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime
from transactions.models import Transaction

@login_required
def dashboard(request):
    # Get current month's start and end dates
    today = timezone.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get user's transactions
    monthly_income = Transaction.objects.filter(
        user=request.user,
        transaction_type='income',
        date__gte=month_start,
        date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense',
        date__gte=month_start,
        date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_balance = Transaction.objects.filter(
        user=request.user
    ).aggregate(
        balance=Sum('amount', filter=Q(transaction_type='income')) -
                Sum('amount', filter=Q(transaction_type='expense'))
    )['balance'] or 0

    # Get recent transactions
    recent_transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')[:5]

    context = {
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'core/dashboard.html', context)

def landing_page(request):
    return render(request, 'core/landing.html')
