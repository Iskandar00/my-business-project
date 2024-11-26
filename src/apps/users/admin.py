from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
    'fullname', 'phone_number', 'role', 'email', 'is_active', 'is_deleted', 'total_balance', 'estimated_balance',
    'number_of_products_sold', 'number_of_products_delivered')

    readonly_fields = ('last_login', 'date_joined', 'total_balance', 'estimated_balance',
                       'number_of_products_sold', 'number_of_products_delivered')

    fields = ('fullname', 'password', 'email', 'phone_number', 'role', 'last_login', 'is_active', 'date_joined', )

    list_display_links = list_display
    search_fields = ('fullname', 'phone_number', 'email')

    list_filter = ('role', 'is_active', 'is_deleted')

    ordering = ('fullname',)


admin.site.register(CustomUser, CustomUserAdmin)
