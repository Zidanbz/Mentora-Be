# mentoraconfig/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# 1. Pindahkan semua import ke bagian atas
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# PENGATURAN KUNCI UNTUK PRODUKSI & DEVELOPMENT
# ==============================================================================

# Ambil SECRET_KEY dari environment variable. Jangan pernah hardcode di sini.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-development')

# DEBUG akan otomatis False saat di-deploy di Render,
# dan True saat dijalankan di komputer lokal.
DEBUG = 'RENDER' not in os.environ

# Atur host yang diizinkan secara dinamis
ALLOWED_HOSTS = []

# Untuk deployment di Render, otomatis tambahkan hostname Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# ==============================================================================
# KONFIGURASI APLIKASI
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd Party Apps
    'rest_framework',
    'corsheaders',

    # Aplikasi Anda
    'accounts',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Middleware CORS diletakkan sedekat mungkin ke atas
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mentoraconfig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mentoraconfig.wsgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    'default': dj_database_url.config(
        # Mengambil DATABASE_URL dari environment variable saat di Render
        # Jika tidak ada, gunakan koneksi ke database lokal Anda
        default=f'postgresql://{os.getenv("DB_USER", "mentorauser")}:{os.getenv("DB_PASSWORD")}@localhost/mentoradb',
        conn_max_age=600
    )
}


# ==============================================================================
# PASSWORD & INTERNATIONALIZATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Makassar' # Anda bisa sesuaikan zona waktu
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC FILES & Lainnya
# ==============================================================================

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Pengaturan Redirect Login & Logout
LOGIN_REDIRECT_URL = '/dashboard/upload-products/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Pengaturan CORS untuk frontend Next.js Anda
# Ganti dengan URL Vercel Anda nanti
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://mentora-be.onrender.com"
    # "https://nama-proyek-frontend-anda.vercel.app", # <-- Ganti ini nanti
]

# ==============================================================================
# KONFIGURASI DJANGO REST FRAMEWORK (DRF)
# ==============================================================================

# TAMBAHKAN BLOK BARU INI DI BAGIAN PALING BAWAH FILE
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
        
        # PERBAIKAN: Nama kelas yang benar adalah 'FileUploadParser' untuk menangani data mentah,
        # atau kita bisa juga membuat parser kustom jika perlu.
        # Untuk kasus menerima teks biasa di body, DRF tidak punya parser bawaan.
        # Namun, kita bisa atasi ini di level view. Untuk sekarang, kita hapus parser yang salah.
    ]
}


