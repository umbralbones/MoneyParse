from django.urls import path
from .views import transaction_list, add_transaction
from . import views

urlpatterns = [
    path('', transaction_list, name='transaction_list'),
    path('add/', add_transaction, name='add_transaction'),
    path('edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),

]
