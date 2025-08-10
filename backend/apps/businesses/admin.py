
from django.contrib import admin
from .models import Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
	list_display = ("name", "city", "business_type", "accessibility_level", "is_verified")
	search_fields = ("name", "city", "description", "address", "postcode")
