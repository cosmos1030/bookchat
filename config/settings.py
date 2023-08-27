from pathlib import Path
from datetime import timedelta

import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.dirname(BASE_DIR)

env = environ.Env(DEBUG=(bool, True))  # 환경 변수를 이용할 수 있는 상태로 세팅
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))  # 어떤 파일에서 불러올건지 결정

OPENAI_KEY = env("OPENAI_KEY")

DEBUG = env("DEBUG")  # 배포시 DEBUG 반드시 끄기!


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)o&hcq=7_3k*!vkupw#nvwyrq^!%5%mfy6@6n$)sy20lqg*p7t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG"))

ALLOWED_HOSTS = [
    ".bookchatting.io",
    ".cloudtype.app",
    ".elasticbeanstalk.com",
    "localhost",
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    # Internal
    "api",
    "common",
    "bookchat",
    'account',
    # External
    "corsheaders",  # cors 에러 방지. 서버와 클라이언트 간 통신을 위함
    "rest_framework",  # api 개발 위함
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "sass_processor",  # scss 컴파일
    "daphne",  # 웹소켓
    "channels",  # 웹소켓 이용을 위한 모듈
    # 'whitenoise.runserver_nostatic'
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

ASGI_APPLICATION = "config.asgi.application"  # config 는 django 프로젝트 이름

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


CORS_ALLOWED_ORIGINS = [  # 실제 배포 시에는 원하는 출처만 허용하도록 설정 (보안 상 주의)
    "http://localhost:3000",  # 리액트 애플리케이션의 주소
    "http://127.0.0.1:3000"
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": "svc.sel4.cloudtype.app",
#         "PORT": "30915",
#         "NAME": "postgresql",
#         "USER": "root",
#         "PASSWORD": env("PASSWORD"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "bookchat", "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, ".static_root/")


SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, ".static_root/")
SASS_OUTPUT_STYLE = "compact"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

MEDIA_URL = "media/"  # pdf 파일 업로드 시 저장 위치
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.CustomUser"

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000/",
    "https://*.cloudtype.app",
    "https://port-0-bookchat-eu1k2llksdf6ji.sel4.cloudtype.app",
]

LOGIN_REDIRECT_URL = "/"  # 자동으로 생성된 login 창에서 로그인 한 후 index 페이지로 가도록 함.
LOGOUT_REDIRECT_URL = "/"

# REST Framework 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT 설정
from datetime import timedelta
# 추가적인 JWT_AUTH 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}