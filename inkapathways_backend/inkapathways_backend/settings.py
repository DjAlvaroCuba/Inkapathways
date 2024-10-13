"""
Django settings for inkapathways_backend project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import environ
from pathlib import Path
from datetime import timedelta
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    # dependencias
    'rest_framework',
    'drf_spectacular',
    
    # Aplicaciones internas

    'api_lugares',
    'api_root',
    'api_users',
    'modelo_v1'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inkapathways_backend.urls'

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

WSGI_APPLICATION = 'inkapathways_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'api_users.authentication.TokenAuthentication',  # Asegúrate de que esto esté correcto
    ),
}
#SIMPLE_JWT = {
#    # Duración del token de acceso
#    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
#    # Duración del token de actualización
#    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#    'ROTATE_REFRESH_TOKENS': True,  # Rotar el token de actualización
#    # Agregar a la lista negra el token de actualización anterior
#    'BLACKLIST_AFTER_ROTATION': True,
#}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Documentacion API / INKAPATHWAYS',
    'DESCRIPTION': 'Viaja con inteligencia: Inka Pathways y su IA predictiva te ayudan a descubrir lo mejor de cada destino, personalizando tu experiencia de viaje con Inteligencia Artificial',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    #'TOS': '',(Terminos y servicios)
    'CONTACT': {
        'name': 'Equipo de soporte',
        'url': '',
        'email': 'Famousalvarocubaporras@gmail.com',
    },
    #'LICENSE': {
    #    'name': 'Licencia',
    #    'url': 'www.inkapathways.com',
    #},
    'SERVERS': [
        {
            'url': 'http://127.0.0.1:8000/',
            'description': 'Servidor principal',
            #'variables': {
            #    'version': {
            #        'default': 'v1',
            #        'description': 'Versión de la API'
            #    }
            #}
        }
        
        #{
        #    'url': 'https://api.inkapathways.com/v2',
        #    'description': 'Servidor de producción 2',
        #    #'variables': {
        #    #    'version': {
        #    #        'default': 'v2',
        #    #        'description': 'Versión de la API V2'
        #    #    }
        #    #}
        #},

       
    ],
    #'TAGS': [
    #    # {'name': 'Turistas', 'description': 'Operaciones sobre turistas'},
    #    # {'name': 'Usuarios', 'description': 'Operaciones sobre usuario'},
    #    # {'name': 'Tripticos', 'description': 'Operaciones sobre tripticos'},
    #    {'name': 'ModeloV1', 'description': 'Operaciones sobre ModeloV1'},
    #],
}
