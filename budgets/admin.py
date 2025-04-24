from django.contrib import admin
from .models import Budget, BudgetItem

class BudgetItemInline(admin.TabularInline):
    model = BudgetItem
    extra = 1

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'amount', 'get_total_items', 'get_remaining_amount', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BudgetItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')