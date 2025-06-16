# dashboard/tests.py

from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch 
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, ChatHistory, Sale # <-- Import Sale
from accounts.models import Company

# Mengubah nama class agar lebih deskriptif untuk seluruh dashboard
class DashboardAPITests(APITestCase):
    
    def setUp(self):
        """
        Setup data tes yang akan digunakan di semua fungsi tes.
        """
        # Buat User dan Perusahaan A dengan dua produk
        self.user_a = User.objects.create_user(username='user_a', password='password123')
        self.company_a = Company.objects.create(name='Toko A Sejahtera', owner=self.user_a)
        self.product_a1 = Product.objects.create(company=self.company_a, name='Kopi Susu', price=18000)
        self.product_a2 = Product.objects.create(company=self.company_a, name='Teh Manis', price=5000)
        refresh_a = RefreshToken.for_user(self.user_a)
        self.token_a = str(refresh_a.access_token)

        # Buat User dan Perusahaan B
        self.user_b = User.objects.create_user(username='user_b', password='password456')
        self.company_b = Company.objects.create(name='Warung B Jaya', owner=self.user_b)
        self.product_b = Product.objects.create(company=self.company_b, name='Nasi Goreng', price=20000)
        refresh_b = RefreshToken.for_user(self.user_b)
        self.token_b = str(refresh_b.access_token)

    # --- Tes untuk API Produk ---
    
    def test_list_products_requires_authentication(self):
        url = reverse('product-list-api')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ Tes keamanan daftar produk berhasil.")

    def test_list_products_returns_only_own_products(self):
        url = reverse('product-list-api')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        print("✅ Tes multi-tenancy untuk daftar produk berhasil.")
        
    def test_create_product_for_own_company(self):
        url = reverse('product-list-api')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        data = {'name': 'Produk A Baru', 'price': 15000}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.filter(company=self.company_a).count(), 3)
        print("✅ Tes pembuatan produk baru berhasil.")

    def test_user_cannot_view_another_companys_product_detail(self):
        url = reverse('product-detail-api', kwargs={'pk': self.product_b.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("✅ Tes keamanan detail produk (antar perusahaan) berhasil.")

    # --- Tes untuk API Chatbot & Riwayat ---

    @patch('dashboard.views.run_chatbot_conversation')
    def test_chatbot_api_works_and_creates_history(self, mock_run_conversation):
        mock_run_conversation.return_value = "Ini adalah jawaban AI palsu."
        url = reverse('chatbot-api')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        data = {'prompt': 'Halo, bot!'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_run_conversation.assert_called_once_with(user_prompt='Halo, bot!', company=self.company_a)
        self.assertEqual(ChatHistory.objects.filter(company=self.company_a).count(), 1)
        print("✅ Tes fungsionalitas Chatbot API berhasil.")

    def test_chat_history_returns_only_own_history(self):
        ChatHistory.objects.create(company=self.company_a, prompt="Prompt A", response="Response A")
        ChatHistory.objects.create(company=self.company_b, prompt="Prompt B", response="Response B")

        url = reverse('chat-history-api')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['prompt'], 'Prompt A')
        print("✅ Tes multi-tenancy untuk riwayat chat berhasil.")
        
    # --- Tes untuk Fitur AI Lanjutan ---

    @patch('dashboard.chatbot_tools.random.choice')
    def test_proactive_suggestion_api(self, mock_random_choice):
        """
        Memastikan API saran proaktif bekerja dan memberikan saran yang relevan.
        """
        # SETUP: Buat data penjualan.
        for _ in range(10):
            Sale.objects.create(company=self.company_a, product=self.product_a1, quantity=1)
        Sale.objects.create(company=self.company_a, product=self.product_a2, quantity=1)

        # 1. PERBAIKAN: Definisikan HANYA inti dari saran yang akan dikembalikan oleh random.choice
        core_suggestion = f"Produk '{self.product_a2.name}' tampaknya kurang diminati bulan ini. Coba tawarkan promo 'Beli 1 Gratis 1' akhir pekan ini untuk meningkatkan penjualannya."
        mock_random_choice.return_value = core_suggestion

        # 2. PERBAIKAN: Bangun string hasil akhir yang kita harapkan, sesuai dengan logika di chatbot_tools.py
        expected_final_suggestion = f"Saran Proaktif: {core_suggestion}"

        url = reverse('proactive-suggestion-api')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        response = self.client.get(url, format='json')

        # Periksa hasilnya
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('suggestion', response.data)
        
        # 3. PERBAIKAN: Bandingkan hasil dari API dengan string akhir yang kita harapkan
        self.assertEqual(response.data['suggestion'], expected_final_suggestion)
        print("✅ Tes API saran proaktif berhasil.")
