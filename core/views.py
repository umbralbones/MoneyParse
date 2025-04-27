from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime
from transactions.models import Transaction
import requests
from django.conf import settings
import re

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

    # Initialize financial advice
    financial_advice = ""

    if request.method == "POST" and "refresh_advice" in request.POST:
        # Check if there is enough data for advice
        has_income = monthly_income > 0
        has_expenses = monthly_expenses > 0
        has_transactions = recent_transactions.exists() if hasattr(recent_transactions, 'exists') else len(recent_transactions) > 0

        if has_income and has_expenses and has_transactions:
            # Compose prompt
            prompt = (
                f"User's monthly income: {monthly_income}\n"
                f"User's monthly expenses: {monthly_expenses}\n"
                f"User's total balance: {total_balance}\n"
                "Recent transactions:\n"
            )
            for t in recent_transactions:
                prompt += f"- {t.date}: {t.transaction_type} {t.amount} ({getattr(t, 'category', 'N/A')})\n"
            prompt += "\nProvide concise, personalized financial advice based on this data. Limit your response to 100 words. Don't format the response with bold or italic."

            # Call Perplexity API
            try:
                response = requests.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "sonar",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 500
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    raw_content = response.json()["choices"][0]["message"]["content"]
                    # Remove citations
                    cleaned_advice = re.sub(r"\[\d+\]", "", raw_content).strip()
                    financial_advice = cleaned_advice
                else:
                    financial_advice = f"Unable to retrieve advice at this time. Got error: {str(response.json())}"
            except Exception as e:
                financial_advice = f"Unable to retrieve advice at this time. Got error: {str(e)}"
        else:
            financial_advice = "Add more transactions and budgets to receive personalized advice!"ce = "Add more transactions and budgets to receive personalized advice!"

    context = {
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'financial_advice': financial_advice
    }
    return render(request, 'core/dashboard.html', context)

def landing_page(request):
    return render(request, 'core/landing.html')
