from django.contrib import admin
from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'business_type', 
        'accessibility_rating', 
        'postcode', 
        'is_verified',
        'is_active',
        'created_at'
    ]
    list_filter = [
        'business_type', 
        'accessibility_rating', 
        'is_verified', 
        'is_active',
        'created_at'
    ]
    search_fields = ['name', 'address', 'postcode', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'business_type', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Location', {
            'fields': ('address', 'postcode', 'latitude', 'longitude', 'what3words')
        }),
        ('Accessibility', {
            'fields': ('accessibility_rating', 'last_assessed', 'assessed_by', 'assessment_notes')
        }),
        ('Business Management', {
            'fields': ('claimed_by', 'is_verified')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Allow filtering by claimed businesses
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('claimed_by', 'assessed_by')
