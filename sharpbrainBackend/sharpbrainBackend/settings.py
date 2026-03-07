import dj_database_url
import os
from dotenv import load_dotenv


load_dotenv()
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set.")



from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!&@!@@o9vh-iby*_q!e6yn4l4^s+4@q8e5r_oogq-my!-g9xrs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['las.pythonanywhere.com', "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sharpbrainApi',
    'rest_framework' ,
    "corsheaders",
    "rest_framework_simplejwt"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',#from whitenoise library ; this is for render setup to avoid issue in the future about static files, though i neva dey use em but django itself have some already
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",#from coresheader library ; the boss Cross Origin Resource Sharing
    "django.middleware.common.CommonMiddleware",#from coresheader library ; the boss Cross Origin Resource Sharing
]

ROOT_URLCONF = 'sharpbrainBackend.urls'

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

WSGI_APPLICATION = 'sharpbrainBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default' : {'ENGINE': 'django.db.backends.postgresql',
    'HOST': os.getenv('DB_HOST'),
    'PORT': os.getenv('DB_PORT'),
    'USER': os.getenv('DB_USER'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
    'NAME': os.getenv('DB_NAME'),
    'CONN_MAX_AGE' : 0,
    'OPTIONS' : {
        'sslmode': 'require',
        'prepare_threshold' : None #since i am using 6543 as my superbase port, i need to stop django from holding unto data each time and force it to just send data and disappear
    }}
    }

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
# }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'lastissa11@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'lastissa11@gmail.com'
EMAIL_PORT = 465


#even though i do not understand this yet, it is for handling all the html, css and js on my proj, i do not ue those noe but django uses em , i had to do this cos of the whitenoise module i imported
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES" : ["rest_framework_simplejwt.authentication.JWTAuthentication"]
}



#i used this for the render build command prompt istead of just using the pip install -r req....
#pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input