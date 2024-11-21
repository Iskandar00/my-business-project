import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-$4w(zunj95wi!k$uq3ta9+=a4u%n0$&6o)8etvl%=@ejmm0v%q'

DEBUG = True

ALLOWED_HOSTS = []

REDIS_PORT_URL = "redis://redis_db:6379"

INSTALLED_APPS = [
    'jazzmin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',
]

INSTALLED_APPS += [
    'apps.general.apps.GeneralConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.bonuses.apps.BonusesConfig',
    'apps.categories.apps.CategoriesConfig',
    'apps.comments.apps.CommentsConfig',
    'apps.contact_us.apps.ContactUsConfig',
    'apps.likes.apps.LikesConfig',
    'apps.links.apps.LinksConfig',
    'apps.notifications.apps.NotificationsConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.payments.apps.PaymentsConfig',
    'apps.products.apps.ProductsConfig',
    'apps.users.apps.UsersConfig',
    'apps.wishlists.apps.WishlistsConfig',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home-page'
LOGOUT_REDIRECT_URL = 'login'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR / 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR / 'media')

AUTH_USER_MODEL = 'users.CustomUser'

