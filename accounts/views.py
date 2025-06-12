# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from .forms import RegistrationForm
from .models import Company, User

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Menggunakan transaction.atomic untuk keamanan data
            with transaction.atomic():
                # Ambil data yang sudah bersih dari form
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                company_name = form.cleaned_data.get('company_name')

                # Buat user baru (gunakan create_user agar password di-hash)
                new_user = User.objects.create_user(username=username, password=password)
                
                # Buat company baru dan hubungkan dengan user yang baru dibuat
                Company.objects.create(name=company_name, owner=new_user)
            
            # Setelah registrasi berhasil, langsung login-kan user
            login(request, new_user)
            
            # Arahkan ke halaman dashboard (atau halaman lain yang sesuai)
            # Untuk sekarang, kita arahkan ke API list produk
            return redirect('product-list-api')
    else:
        form = RegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form})
