# dashboard/serializers.py
from rest_framework import serializers
from .models import Product, ChatHistory

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'created_at']
        read_only_fields = ['company']
        
# === TAMBAHKAN SERIALIZER BARU DI BAWAH INI ===
class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        # Tentukan field yang ingin kita tampilkan di API
        fields = ['id', 'prompt', 'response', 'created_at']
