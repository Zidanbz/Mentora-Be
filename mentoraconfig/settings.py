# mentoraconfig/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# 1. Semua import berada di atas
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# PENGATURAN KUNCI UNTUK PRODUKSI & DEVELOPMENT
# ==============================================================================

# Mengambil SECRET_KEY dari environment variable.
# Fallback ke kunci yang tidak aman HANYA untuk development lokal.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-for-development')

# DEBUG akan otomatis False saat di-deploy di Render.
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

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
    # Tambahkan WhiteNoise di bawah staticfiles agar bisa melayani file CSS Admin
    'whitenoise.runserver_nostatic',
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
    # Tambahkan middleware WhiteNoise di posisi kedua
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mentoraconfig.urls'
WSGI_APPLICATION = 'mentoraconfig.wsgi.application'

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

# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    'default': dj_database_url.config(
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

LANGUAGE_CODE = 'id-id'
TIME_ZONE = 'Asia/Makassar'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC FILES (PENTING UNTUK TAMPILAN ADMIN)
# ==============================================================================

STATIC_URL = 'static/'
# Menentukan folder pusat tempat `collectstatic` akan mengumpulkan semua file
STATIC_ROOT = BASE_DIR / "staticfiles"
# Menambahkan metode penyimpanan WhiteNoise yang efisien
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ==============================================================================
# PENGATURAN LAINNYA
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/dashboard/upload-products/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # "https://nama-frontend-anda.vercel.app", # Ganti ini nanti setelah frontend di-deploy
]

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
    ]
}
