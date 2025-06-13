# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL untuk daftar produk (GET, POST)
    path('', views.product_list_api, name='product-list-api'),

    # URL BARU untuk satu produk spesifik (GET, PUT, DELETE)
    path('<int:pk>/', views.product_detail_api, name='product-detail-api'),
       # URL BARU untuk chatbot
    path('chatbot/', views.chatbot_api, name='chatbot-api'),
    # URL BARU untuk Riwayat Chat
    path('chat-history/', views.chat_history_api, name='chat-history-api'),
    # URL BARU untuk halaman upload
    path('upload-products/', views.upload_products_view, name='upload-products'),
    
]