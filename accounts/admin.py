# accounts/admin.py
from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
