from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_list, name='budget_list'),
    path('create/', views.budget_create, name='budget_create'),
    path('<int:pk>/', views.budget_detail, name='budget_detail'),
    path('<int:pk>/edit/', views.budget_edit, name='budget_edit'),
    path('<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    path('<int:budget_pk>/items/<int:item_pk>/delete/', 
         views.budget_item_delete, name='budget_item_delete'),
]
