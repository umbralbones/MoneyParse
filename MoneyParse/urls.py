from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('transactions/', include('transactions.urls')),
    path('budgets/', include('budgets.urls')),
]