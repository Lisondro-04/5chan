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

    # Seguridad
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Middleware de Axes (bloqueo tras múltiples intentos fallidos)
    'axes.middleware.AxesMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware OAuth2 (para request.user vía token)
    'oauth2_provider.middleware.OAuth2TokenMiddleware',

    # Middleware de simple-history (auditoría de cambios)
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

# Autenticación con backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',         # Principal
    'axes.backends.AxesBackend',                         # Seguridad (bloqueo)
    'oauth2_provider.backends.OAuth2Backend',            # Para tokens OAuth2
)

# Configuración de django-axes
AXES_FAILURE_LIMIT = 5                    # Intentos fallidos antes del bloqueo
AXES_COOLOFF_TIME = 0                     # Tiempo (en horas) hasta desbloqueo automático
AXES_RESET_ON_SUCCESS = True              # Restablecer el contador al iniciar sesión con éxito
AXES_LOCKOUT_TEMPLATE = 'axes/lockout.html'  # Vista personalizada para bloqueo
