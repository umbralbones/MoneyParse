from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # for signup
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('', include('core.urls')),  # landing page for MoneyParse
    path('transactions/', include('transactions.urls')),
]