from pathlib import Path
import os
import environ  # ✅ Import django-environ

# ✅ Initialize environ
env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))  # Load .env file

# ✅ Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Use values from .env
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# ✅ Application definition
INSTALLED_APPS = [
    'django_user_agents',
    'rest_framework',
    'urlshortener',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ✅ CORS Middleware must be first or near the top
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'fuzzyurlpro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fuzzyurlpro.wsgi.application'

# ✅ Database Configuration (Now using .env variables)
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# ✅ Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ✅ Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static and Media Files
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ GeoIP for user analytics
GEOIP_PATH = BASE_DIR / 'geoip'  # Ensure this directory exists

# ✅ Your site's base URL (used in generating short URLs + QR codes)
SITE_DOMAIN = env('SITE_DOMAIN', default='http://127.0.0.1:8000')  # Read from .env

# ✅ Default Primary Key Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ CORS CONFIGURATION - Allow React frontend to call Django APIs
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=True)


# Allow API requests from frontend without CSRF issues
 # Allows requests from any frontend (React, Postman, etc.)
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000"]  # Trust localhost for API calls
CSRF_COOKIE_SECURE = False  # Allow CSRF cookies for development
CSRF_COOKIE_HTTPONLY = False  # Ensure CSRF cookies can be sent via frontend
CSRF_COOKIE_SAMESITE = 'None'  # Avoid same-site cookie restrictions for APIs

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:8000"]
