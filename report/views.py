# report/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from django.utils import timezone
from collections import defaultdict
from datetime import timedelta



@login_required
def report_home(request):
    return render(request, 'report/report_home.html')

def _build_time_series(qs, span_days):
    """
    Given a queryset of Transactions, return two lists:
      - labels: list of dates as 'YYYY-MM-DD' for the last span_days days
      - data:  list of sums of amounts on each date
    """
    today = timezone.localdate()
    # init zeroed map for each of the last N days
    sums = defaultdict(float)
    for tx in qs:
        d = tx.date  # assuming tx.date is a DateTimeField
        sums[d] += float(tx.amount)

    labels = []
    data   = []
    for i in range(span_days - 1, -1, -1):
        d = today - timedelta(days=i)
        labels.append(d.isoformat())
        data.append(sums[d])
    return labels, data

@login_required
def report_weekly(request):
    span = 7
    base_qs = Transaction.objects.filter(user=request.user, date__gte=timezone.now() - timedelta(days=span))
    inc_qs  = base_qs.filter(transaction_type='income')
    exp_qs  = base_qs.filter(transaction_type='expense')

    inc_labels, inc_data = _build_time_series(inc_qs, span)
    exp_labels, exp_data = _build_time_series(exp_qs, span)
    # totals for the indicator
    total_inc = sum(inc_data)
    total_exp = sum(exp_data)

    return render(request, 'report/report_weekly.html', {
        'inc_labels': inc_labels,
        'inc_data':   inc_data,
        'exp_data':   exp_data,
        'total_inc':  total_inc,
        'total_exp':  total_exp,
        'weekly_income_transactions': inc_qs,
        'weekly_expense_transactions': exp_qs,
    })

@login_required
def report_monthly(request):
    today = timezone.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    span = (today.date() - month_start.date()).days + 1

    base_qs = Transaction.objects.filter(user=request.user, date__gte=month_start)
    inc_qs  = base_qs.filter(transaction_type='income')
    exp_qs  = base_qs.filter(transaction_type='expense')

    inc_labels, inc_data = _build_time_series(inc_qs, span)
    exp_labels, exp_data = _build_time_series(exp_qs, span)
    total_inc = sum(inc_data)
    total_exp = sum(exp_data)

    return render(request, 'report/report_monthly.html', {
        'inc_labels': inc_labels,
        'inc_data':   inc_data,
        'exp_data':   exp_data,
        'total_inc':  total_inc,
        'total_exp':  total_exp,
        'monthly_income_transactions': inc_qs,
        'monthly_expense_transactions': exp_qs,
    })


