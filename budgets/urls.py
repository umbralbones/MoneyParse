from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.budget_create, name='budget_create'),
    path('<int:pk>/edit/', views.budget_edit, name='budget_edit'),
    path('<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    path('<int:budget_pk>/items/<int:item_pk>/delete/', views.item_delete, name='item_delete'),
    path('<int:pk>/', views.budget_detail, name='budget_detail'),
    path('', views.budgets, name='budgets'),
]