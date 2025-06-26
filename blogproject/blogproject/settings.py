from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ukz72g)*267@$nvdk**+6#+a*nyzh_1t3o2=@wxtpga$cew)2^'
DEBUG = True
ALLOWED_HOSTS = [
    '192.168.50.236',
    'local_host',
    '127.0.0.1'
]

INSTALLED_APPS = [
    # Apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps del proyecto
    'blogapp',
    'widget_tweaks',
    'ckeditor',

    # OAuth2 Toolkit
    'oauth2_provider',

    # Auditoría de modelos
    'simple_history',
    'axes'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    #Middleware de Axes (monitorea los inicios de sesión fallidos y bloquea usuarios)
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # OAuth2 Token Middleware (para request.user vía token)
    'oauth2_provider.middleware.OAuth2TokenMiddleware',

    # Middleware de simple-history (guarda el usuario en cada cambio)
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'blogproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'blogapp' / 'templates' / 'blogapp',
        ],
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

WSGI_APPLICATION = 'blogproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = None  # Django busca logout.html al cerrar sesión

# OAuth2 Toolkit
AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

#Configuración de Axes
AXES_FAILURE_LIMIT = 5 #intentos previos al bloqueo
AXES_COOLOFF_TIME = 0 #en horas (desbloqueo automático)
AXES_RESET_ON_SUCCESS = True #Limpia intentos fallidos si el login fue exitoso
AXES_LOOKOUT_TEMPLATE = 'axes/lockout.html' #vista de bloqueo
