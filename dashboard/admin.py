# dashboard/admin.py
from django.contrib import admin
from .models import Product, ChatHistory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Menampilkan kolom-kolom penting di daftar produk
    list_display = ('name', 'company', 'price', 'created_at')
    # Menambahkan filter berdasarkan perusahaan
    list_filter = ('company',)
    # Menambahkan fitur pencarian
    search_fields = ('name', 'company__name')

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('company', 'prompt_snippet', 'response_snippet', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('prompt', 'response', 'company__name')
    readonly_fields = ('company', 'prompt', 'response', 'created_at')

    def prompt_snippet(self, obj):
        # Menampilkan potongan prompt agar tidak terlalu panjang
        return obj.prompt[:50] + '...' if len(obj.prompt) > 50 else obj.prompt
    
    def response_snippet(self, obj):
        # Menampilkan potongan respons
        return obj.response[:50] + '...' if len(obj.response) > 50 else obj.response
    
    prompt_snippet.short_description = 'Prompt'
    response_snippet.short_description = 'Response'

