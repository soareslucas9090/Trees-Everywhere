import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


SPECTACULAR_SETTINGS = {
    "TITLE": "Tree Everywhere",
    "DESCRIPTION": "Projeto desenvolvido para desafio técnico da YouShop",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}


SECRET_KEY = os.environ.get("secretKeyDjango")

# Testa se já há variáveis de ambiente configuradas, se não há, carrega do arquivo local .env
if not SECRET_KEY:
    load_dotenv()
    SECRET_KEY = os.environ.get("secretKeyDjango")

DEBUG = os.environ.get("debugMode")
ALLOWED_HOSTS = [os.environ.get("allowedHosts")]
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("bdEngine"),
        "NAME": os.environ.get("bdName"),
        "USER": os.environ.get("bdUser"),
        "PASSWORD": os.environ.get("bdPass"),
        "HOST": os.environ.get("bdHost"),
        "PORT": os.environ.get("bdPort"),
    }
}
signing_key = os.environ.get("secretKeyJWT")


if "test" in sys.argv or "test_coverage" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }

AUTH_USER_MODEL = "everywhere.User"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


CORS_ORIGIN_WHITELIST = [
    "https://web-vurkazv8fljz.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
    "http://127.0.0.1",
    "https://127.0.0.1",
]

CORS_ALLOWED_HOSTS = [
    "https://web-vurkazv8fljz.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
    "http://127.0.0.1",
    "https://127.0.0.1",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://web-vurkazv8fljz.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
    "http://127.0.0.1",
    "https://127.0.0.1",
]

CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOW_METHODS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "everywhere",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "trees.urls"

INTERNAL_IPS = [
    "127.0.0.1",
    "https://web-vurkazv8fljz.up-de-fra1-k8s-1.apps.run-on-seenode.com",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "trees.wsgi.application"

# redirecionamento padrão depois de fazer o login
LOGIN_REDIRECT_URL = "/"

SESSION_COOKIE_AGE = 300

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/


LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DATE_INPUT_FORMATS": ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"],
    "TIME_INPUT_FORMATS": [
        "%H:%M",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=140),
    "BLACKLIST_AFTER_ROTATION": False,
    "SIGNING_KEY": signing_key,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
