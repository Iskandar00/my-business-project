from django.contrib import admin
from apps.features.models import Feature, FeatureValue


class FeatureValueInline(admin.TabularInline):
    """Inline feature values for a Feature."""
    model = FeatureValue
    extra = 8
    fields = ('value', 'slug')
    prepopulated_fields = {'slug': ('value',)}


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """Admin configuration for the Feature model."""
    list_display = ('name', 'main_category', 'sub_category',)
    list_display_links = list_display
    list_filter = ('main_category', 'sub_category')
    search_fields = ('name', 'slug', 'main_category__name', 'sub_category__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FeatureValueInline]

    def get_queryset(self, request):
        """Optimize queries for admin display."""
        queryset = super().get_queryset(request)
        return queryset.select_related('main_category', 'sub_category')


@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    """Admin configuration for the FeatureValue model."""
    list_display = ('feature', 'value', 'slug')
    list_filter = ('feature',)
    search_fields = ('feature__name', 'value', 'slug')
    prepopulated_fields = {'slug': ('value',)}
