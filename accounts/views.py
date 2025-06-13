# accounts/views.py

from django.shortcuts import redirect
from django.http import JsonResponse # <-- 2. Pindahkan import ini ke atas
import json # <-- 1. Pindahkan import ini ke atas

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Company

@csrf_exempt
def register_view(request):
    """
    API endpoint untuk registrasi user dan perusahaan baru.
    """
    if request.method != 'POST':
        # Jika metodenya bukan POST, langsung tolak.
        return JsonResponse({'error': 'Metode GET tidak diizinkan untuk endpoint ini.'}, status=405)

    try:
        # Coba parsing data JSON dari body request
        data = json.loads(request.body)
        username = data.get('username')
        company_name = data.get('company_name')
        password = data.get('password')

        # Validasi sederhana
        if not all([username, company_name, password]):
            return JsonResponse({'error': 'Field username, company_name, dan password wajib diisi.'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username ini sudah digunakan.'}, status=400)

        # Gunakan transaction.atomic untuk memastikan keduanya berhasil dibuat
        with transaction.atomic():
            new_user = User.objects.create_user(username=username, password=password)
            Company.objects.create(name=company_name, owner=new_user)
        
        # Kembalikan pesan sukses
        return JsonResponse({
            'success': f'User {username} dan perusahaan {company_name} berhasil dibuat.'
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Format body request harus JSON yang valid.'}, status=400)
    except Exception as e:
        # Menangkap error lain yang mungkin terjadi
        return JsonResponse({'error': f'Terjadi error internal: {str(e)}'}, status=500)
