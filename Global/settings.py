"""
Django settings for Global project.
"""

from pathlib import Path
import os
import dj_database_url
import json # ⬅️ IMPORTACIÓN NECESARIA PARA DECODIFICAR JSON

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

HANDLER_404 = 'gestion_web.views.handler404'

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')
DEBUG = 'RENDER' not in os.environ
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME' )
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS. append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    # 🎨 AGREGADO PARA EL TEMA VISUAL DEL ADMIN (DEBE SER LA PRIMERA APP)
    'jazzmin', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'CasaReposo',
    # ☁️ AGREGADO PARA ALMACENAMIENTO EXTERNO (GCS)
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Global.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'Global.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'es-cl' # Español de Chile
TIME_ZONE = 'America/Santiago' # Zona horaria de Santiago

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [STATIC_DIR]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ----------------------------------------------------------------------
# 📧 CONFIGURACIÓN DE CORREO ELECTRÓNICO (SMTP) 📧
# ----------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = 'jairletelier23@gmail.com' 
EMAIL_HOST_PASSWORD = 'ufbq plwa nzvi drsm' 
DEFAULT_FROM_EMAIL = 'Casa de Reposo Mi Hogar <tu_correo_de_envio@ejemplo.com>'

# ----------------------------------------------------------------------
# 🔑 CONFIGURACIÓN DE REDIRECCIÓN DE AUTENTICACIÓN 🔑
# ----------------------------------------------------------------------
LOGOUT_REDIRECT_URL = '/login/' 

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')

# ----------------------------------------------------------------------
# ☁️ CONFIGURACIÓN DE ALMACENAMIENTO MEDIA (GOOGLE CLOUD STORAGE - GCS) ☁️
# ----------------------------------------------------------------------
# Se usa si DEBUG=False (en Render). Requiere la tarjeta de verificación de GCP.
if not DEBUG:
    # 1. Almacenamiento por defecto: usa Google Cloud Storage
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    
    # 2. El nombre de tu Bucket (Contenedor) de GCS
    GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
    
    # 3. 💥 SOLUCIÓN CRÍTICA: Decodificación explícita de la clave JSON
    # Leemos la cadena de texto de la variable de entorno
    credentials_string = os.environ.get('GS_CREDENTIALS_JSON')
    
    # Intentamos convertir la cadena de texto en un objeto JSON (diccionario)
    if credentials_string:
        try:
            GS_CREDENTIALS = json.loads(credentials_string)
        except json.JSONDecodeError as e:
            # En caso de error de formato JSON, se desactiva la credencial
            print("ERROR FATAL de JSON en GS_CREDENTIALS_JSON. Revise los saltos de línea.")
            GS_CREDENTIALS = None
    else:
        GS_CREDENTIALS = None


    # 4. Configuración de la URL para mostrar los archivos
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
    
# ----------------------------------------------------
# 🎨 CONFIGURACIÓN DE JAZZMIN (TEMA DE ADMIN) 🎨
# ----------------------------------------------------
JAZZMIN_SETTINGS = {
    # Título que aparece en la barra de navegación superior (Usando el nombre guardado)
    "site_title": "CR Mi Hogar Admin", 
    
    # Título que aparece en la pestaña del navegador
    "site_header": "Casa de Reposo “Mi Hogar”",

    # Logo del sitio (opcional, si lo deseas)
    # "site_logo": "images/logo.png", 
    
    # URL de la página principal
    "site_url": "/", 

    # Configuración de UI/UX
    "show_sidebar": True,
    "navigation_expanded": True,
    "navbar_fixed": True,
    "sidebar_fixed": True,
    
    # Temas de interfaz (Opcional: puedes cambiar a 'darkly', 'cosmo', etc.)
    # Aquí seleccionamos un tema de base oscuro moderno:
    "theme": "darkly", 
    "dark_mode_theme": "darkly", 
    
    "show_ui_builder": False, # Desactiva el builder para usuarios finales
}
# ----------------------------------------------------------------------