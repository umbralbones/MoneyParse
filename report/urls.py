from django.urls import path
from .views import report_home
from . import views

urlpatterns = [
    path('', report_home, name='report_home'),
    path('weekly/', views.report_weekly, name='report_weekly' ),
    path('monthly/', views.report_monthly, name='report_monthly' ),
]