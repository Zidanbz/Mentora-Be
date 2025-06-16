# dashboard/tests.py

from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ChatHistory, Product
from accounts.models import Company

class ProductAPITests(APITestCase):
    
    def setUp(self):
        """
        Setup data tes yang akan digunakan di semua fungsi tes.
        Dijalankan sebelum setiap tes.
        """
        # Buat User dan Perusahaan A
        self.user_a = User.objects.create_user(username='user_a', password='password123')
        self.company_a = Company.objects.create(name='Toko A Sejahtera', owner=self.user_a)
        self.product_a = Product.objects.create(company=self.company_a, name='Produk A', price=10000)

        # Buat User dan Perusahaan B
        self.user_b = User.objects.create_user(username='user_b', password='password456')
        self.company_b = Company.objects.create(name='Warung B Jaya', owner=self.user_b)
        self.product_b = Product.objects.create(company=self.company_b, name='Produk B', price=20000)

        # Siapkan token untuk User A untuk digunakan di tes-tes selanjutnya
        refresh = RefreshToken.for_user(self.user_a)
        self.token_a = str(refresh.access_token)

    def test_list_products_requires_authentication(self):
        """
        Memastikan endpoint daftar produk tidak bisa diakses tanpa token.
        """
        url = reverse('product-list-api')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ Tes keamanan daftar produk berhasil.")

    def test_list_products_returns_only_own_products(self):
        """
        Memastikan User A hanya melihat produk milik Perusahaan A.
        """
        url = reverse('product-list-api')
        # Autentikasi sebagai User A dengan menyertakan token di header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Harus ada 1 produk
        self.assertEqual(len(response.data), 1)
        # Pastikan produk yang muncul adalah Produk A
        self.assertEqual(response.data[0]['name'], 'Produk A')
        print("✅ Tes multi-tenancy untuk daftar produk berhasil.")
        
    def test_create_product_for_own_company(self):
        """
        Memastikan User A bisa membuat produk baru untuk Perusahaan A.
        """
        url = reverse('product-list-api')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        
        data = {'name': 'Produk A Baru', 'price': 15000}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Periksa apakah total produk Perusahaan A sekarang menjadi 2
        self.assertEqual(Product.objects.filter(company=self.company_a).count(), 2)
        print("✅ Tes pembuatan produk baru berhasil.")

    def test_user_cannot_view_another_companys_product_detail(self):
        """
        Memastikan User A tidak bisa melihat detail Produk B.
        """
        # URL untuk detail Produk B (milik User B)
        url = reverse('product-detail-api', kwargs={'pk': self.product_b.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        response = self.client.get(url, format='json')
        
        # Harus mengembalikan 404 Not Found karena produk itu tidak ada 'untuk user ini'
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("✅ Tes keamanan detail produk (antar perusahaan) berhasil.")

    @patch('dashboard.views.run_chatbot_conversation')
    def test_chatbot_api_works_and_creates_history(self, mock_run_conversation):
        """
        Memastikan chatbot API bisa dipanggil, memanggil service, dan menyimpan riwayat.
        """
        # Konfigurasi mock untuk mengembalikan jawaban palsu agar tidak memanggil Gemini
        mock_run_conversation.return_value = "Ini adalah jawaban AI palsu."
        
        url = reverse('chatbot-api')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        data = {'prompt': 'Halo, bot!'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], "Ini adalah jawaban AI palsu.")
        
        # Periksa apakah fungsi 'run_chatbot_conversation' dipanggil dengan benar
        mock_run_conversation.assert_called_once_with(user_prompt='Halo, bot!', company=self.company_a)
        
        # Periksa apakah riwayat chat tersimpan di database untuk Perusahaan A
        self.assertEqual(ChatHistory.objects.filter(company=self.company_a).count(), 1)
        history = ChatHistory.objects.get(company=self.company_a)
        self.assertEqual(history.prompt, 'Halo, bot!')
        print("✅ Tes fungsionalitas Chatbot API berhasil.")

    def test_chat_history_returns_only_own_history(self):
        """
        Memastikan endpoint riwayat chat hanya mengembalikan data milik perusahaan yang login.
        """
        # Buat entri riwayat untuk kedua perusahaan
        ChatHistory.objects.create(company=self.company_a, prompt="Prompt A", response="Response A")
        ChatHistory.objects.create(company=self.company_b, prompt="Prompt B", response="Response B")

        url = reverse('chat-history-api')
        # Autentikasi sebagai User A
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_a}')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Harus hanya ada 1 riwayat yang kembali
        self.assertEqual(len(response.data), 1)
        # Pastikan riwayat yang muncul adalah milik Perusahaan A
        self.assertEqual(response.data[0]['prompt'], 'Prompt A')
        print("✅ Tes multi-tenancy untuk riwayat chat berhasil.")
