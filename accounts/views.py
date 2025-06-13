# accounts/views.py

from django.http import JsonResponse, HttpResponse # <-- 1. Tambahkan HttpResponse
import json

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Company

@csrf_exempt
def register_view(request):
    """
    API endpoint untuk registrasi user dan perusahaan baru.
    """
    # ... (kode view registrasi Anda yang sudah ada tetap di sini) ...
    if request.method != 'POST':
        return JsonResponse({'error': 'Metode GET tidak diizinkan untuk endpoint ini.'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        company_name = data.get('company_name')
        password = data.get('password')
        if not all([username, company_name, password]):
            return JsonResponse({'error': 'Field username, company_name, dan password wajib diisi.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username ini sudah digunakan.'}, status=400)
        with transaction.atomic():
            new_user = User.objects.create_user(username=username, password=password)
            Company.objects.create(name=company_name, owner=new_user)
        return JsonResponse({
            'success': f'User {username} dan perusahaan {company_name} berhasil dibuat.'
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Format body request harus JSON yang valid.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Terjadi error internal: {str(e)}'}, status=500)


# =======================================================
# === TAMBAHKAN FUNGSI BARU DI BAWAH INI ===
# =======================================================
def make_me_superuser(request):
    """
    View rahasia untuk menjadikan user yang sudah ada sebagai superuser.
    """
    # Ambil username dari parameter query, contoh: /url-rahasia/?username=zidan
    username = request.GET.get('username')
    if not username:
        return HttpResponse("<h1>Error!</h1><p>Tolong tambahkan `?username=NAMAUSERANDA` di akhir URL.</p>", status=400)
    
    try:
        user_to_upgrade = User.objects.get(username=username)
        user_to_upgrade.is_staff = True
        user_to_upgrade.is_superuser = True
        user_to_upgrade.save()
        return HttpResponse(f"<h1>Sukses!</h1><p>User '{username}' sekarang adalah superuser. Anda bisa login ke halaman admin.</p>")
    except User.DoesNotExist:
        return HttpResponse(f"<h1>Error!</h1><p>User dengan nama '{username}' tidak ditemukan di database.</p>", status=404)

