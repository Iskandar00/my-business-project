from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import General


class GeneralAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'phone_number')
    list_display_links = list_display

    def has_add_permission(self, request):

        if General.objects.exists():
            return False
        return True

    def save_model(self, request, obj, form, change):
        if not change and General.objects.exists():
            raise ValidationError("Only one instance of General can be created.")
        super().save_model(request, obj, form, change)


admin.site.register(General, GeneralAdmin)
