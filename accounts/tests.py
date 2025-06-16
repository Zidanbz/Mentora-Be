# accounts/tests.py

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Company

class AccountAPITests(APITestCase):
    
    def test_successful_user_registration(self):
        """
        Memastikan pengguna baru dapat mendaftar dengan sukses melalui API.
        """
        # URL untuk endpoint registrasi
        url = reverse('register')
        
        # Data yang akan kita kirim untuk mendaftar
        data = {
            'username': 'testuser',
            'company_name': 'Test Company',
            'password': 'strongpassword123'
        }

        # Kirim request POST ke endpoint
        response = self.client.post(url, data, format='json')

        # 1. Periksa apakah status code adalah 201 CREATED (berhasil dibuat)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. Periksa apakah user benar-benar dibuat di database
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

        # 3. Periksa apakah perusahaan benar-benar dibuat dan terhubung
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'Test Company')
        
        # 4. Periksa apakah user yang dibuat adalah pemilik perusahaan
        self.assertEqual(User.objects.get().company, Company.objects.get())
        print("✅ Tes registrasi pengguna berhasil.")


    def test_successful_login_and_token_obtain(self):
        """
        Memastikan pengguna yang sudah ada dapat login dan mendapatkan JWT token.
        """
        # SETUP: Pertama, kita buat user dan perusahaan secara manual untuk di-test
        test_user = User.objects.create_user(username='loginuser', password='password123')
        Company.objects.create(name='Login Corp', owner=test_user)

        # URL untuk endpoint login (mendapatkan token)
        url = reverse('token_obtain_pair')

        # Data yang akan kita kirim untuk login
        data = {
            'username': 'loginuser',
            'password': 'password123'
        }

        # Kirim request POST ke endpoint
        response = self.client.post(url, data, format='json')

        # 1. Periksa apakah status code adalah 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Periksa apakah respons berisi 'access' dan 'refresh' token
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        print("✅ Tes login dan perolehan token berhasil.")

