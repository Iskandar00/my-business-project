from django.contrib import admin

from apps.payments.models import AdminPayment


@admin.register(AdminPayment)
class AdminPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'amount_of_money', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'card_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)