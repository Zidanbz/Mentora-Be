# dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required # <-- 1. Import decorator login_required

# Imports untuk DRF
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes # <-- 2. Import permission_classes
from rest_framework.permissions import IsAuthenticated # <-- 3. Import IsAuthenticated
from rest_framework.response import Response

# Imports untuk aplikasi ini
from .models import Product, ChatHistory
from .serializers import ProductSerializer, ChatHistorySerializer
from .chatbot_service import run_chatbot_conversation
from .forms import UploadFileForm
import pandas as pd


# === API Views (Sekarang Aman) ===

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) # <-- 4. Terapkan aturan: hanya user terautentikasi yang bisa akses
def product_list_api(request):
    """
    API untuk mendapatkan daftar produk MILIK PERUSAHAAN user atau membuat produk baru.
    """
    # Ambil perusahaan milik user yang sedang login
    user_company = request.user.company

    if request.method == 'GET':
        # 5. FILTER data: hanya ambil produk milik perusahaan ini
        products = Product.objects.filter(company=user_company)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # 6. INJECT data: saat menyimpan, otomatis isi 'company' dengan perusahaan user
            serializer.save(company=user_company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) # <-- Terapkan aturan keamanan di sini juga
def product_detail_api(request, pk):
    """
    API untuk mengambil, update, atau hapus satu produk SPESIFIK MILIK PERUSAHAAN user.
    """
    user_company = request.user.company
    try:
        # 7. FILTER saat mengambil data: pastikan produk ada DAN milik perusahaan ini
        product = Product.objects.get(id=pk, company=user_company)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Logika GET, PUT, DELETE selanjutnya sudah otomatis aman karena produk sudah difilter
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    # ... (sisa logika PUT dan DELETE tetap sama) ...
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ... (chatbot_api akan kita amankan di langkah selanjutnya) ...
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_api(request):
    """
    API endpoint untuk chatbot AI yang aman dan menyimpan riwayat.
    """
    user_prompt = ""
    
    if isinstance(request.data, dict):
        user_prompt = request.data.get('prompt', '')
    elif isinstance(request.data, str):
        user_prompt = request.data
    
    user_prompt = user_prompt.strip()

    if not user_prompt:
        return Response(
            {"error": "Prompt tidak boleh kosong."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1. Ambil perusahaan dari user yang sedang login
    user_company = request.user.company

    # 2. PERBAIKAN UTAMA: Kirim 'company' sebagai argumen
    chatbot_response = run_chatbot_conversation(user_prompt=user_prompt, company=user_company)

    # 3. Simpan percakapan ke database
    ChatHistory.objects.create(
        company=user_company,
        prompt=user_prompt,
        response=chatbot_response
    )

    # 4. Kembalikan jawaban
    return Response({"response": chatbot_response})


# === Regular Django Views (Sekarang Aman) ===

def handle_uploaded_excel(file, company): # <-- 8. Tambahkan 'company' sebagai parameter
    """Fungsi helper yang sekarang company-aware."""
    try:
        df = pd.read_excel(file)
        if 'Nama Produk' not in df.columns or 'Harga' not in df.columns:
            raise ValueError("File Excel harus memiliki kolom 'Nama Produk' dan 'Harga'")

        for index, row in df.iterrows():
            # 9. Gunakan 'company' yang diterima untuk membuat produk
            Product.objects.create(
                company=company,
                name=row['Nama Produk'],
                price=row['Harga']
            )
        return {"status": "success", "message": f"{len(df)} produk berhasil diimpor."}
    except Exception as e:
        return {"status": "error", "message": f"Terjadi error: {e}"}


@login_required # <-- 10. Terapkan decorator: view ini hanya bisa diakses user yang login
def upload_products_view(request):
    """
    View untuk halaman upload file, sekarang aman.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 11. Kirim perusahaan user ke fungsi helper
            result = handle_uploaded_excel(request.FILES['file'], request.user.company)
            if result['status'] == 'success':
                messages.success(request, result['message'])
            else:
                messages.error(request, result['message'])
            return redirect('upload-products')
    else:
        form = UploadFileForm()
    
    return render(request, 'dashboard/upload_page.html', {'form': form})

# ================================================
# === CUKUP SALIN DAN TEMPEL BLOK DI BAWAH INI ===
# ================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history_api(request):
    """
    API untuk mengambil daftar riwayat percakapan chatbot
    milik perusahaan yang sedang login.
    """
    # 1. Ambil perusahaan dari user yang sedang login
    user_company = request.user.company

    # 2. Filter riwayat chat berdasarkan perusahaan
    history = ChatHistory.objects.filter(company=user_company)

    # 3. Ubah data menjadi JSON menggunakan serializer
    serializer = ChatHistorySerializer(history, many=True)

    # 4. Kembalikan data
    return Response(serializer.data)
