from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.budget_create, name='budget_create'),
    path('<int:pk>/edit/', views.budget_edit,   name='budget_edit'),
    path('<int:pk>/',     views.budget_detail, name='budget_detail'),
    path('', views.budgets, name='budgets'),

]