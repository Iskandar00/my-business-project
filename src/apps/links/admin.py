from django.contrib import admin
from apps.links.models import Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id_generate', 'user', 'product', 'title', 'created_at')
    list_display_links = list_display
    list_filter = ('user', 'product', 'created_at')
    search_fields = ('id_generate', 'title', 'user__username', 'product__name')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'product')
