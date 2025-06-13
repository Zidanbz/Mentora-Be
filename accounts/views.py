# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
# 1. Import decorator csrf_exempt
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm
from .models import Company, User


# 2. Tambahkan decorator @csrf_exempt di atas fungsi view
@csrf_exempt
def register_view(request):
    # Kita harus menambahkan pengecekan ini karena csrf_exempt
    # hanya bekerja pada view berbasis fungsi, bukan APIView DRF
    if request.method == 'POST':
        # Kita tidak lagi menggunakan Django Forms di sini karena ini adalah API.
        # Kita akan memproses data JSON secara manual.
        import json
        try:
            data = json.loads(request.body)
            username = data.get('username')
            company_name = data.get('company_name')
            password = data.get('password')

            # Validasi sederhana
            if not all([username, company_name, password]):
                return JsonResponse({'error': 'Semua field wajib diisi.'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username sudah digunakan.'}, status=400)

            with transaction.atomic():
                new_user = User.objects.create_user(username=username, password=password)
                Company.objects.create(name=company_name, owner=new_user)
            
            # Kita tidak bisa login via API seperti ini, tapi kita bisa kembalikan pesan sukses
            return JsonResponse({'success': f'User {username} dan perusahaan {company_name} berhasil dibuat.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON tidak valid.'}, status=400)
    
    # Jika metodenya GET, kita beri tahu bahwa ini hanya untuk POST
    from django.http import JsonResponse
    return JsonResponse({'error': 'Metode GET tidak diizinkan untuk endpoint ini.'}, status=405)

