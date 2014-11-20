"""
Django settings for devops project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.core.exceptions import ImproperlyConfigured
try:
    import settings_secret as _secret_settings
except:
    _secret_settings = None


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_secret(secret, default=None):
    """
    return the secret setting stored on the local machine,
    outside of version control. Currently, this is done in
    a file called ./devops/settings_secret.py.
    However, we can convert to env variables at any time.

    will return default if doesn't exist in secret_settings
    and default provided. if no default, will raise error.
    """
    try:
        return getattr(_secret_settings, secret)
    except:
        if default is not None:
            return default
        else:
            msg = "secret, {}, not set".format(secret)
            raise ImproperlyConfigured(msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'core.User'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'core.backends.GitHubEnterprise',
    'social.backends.github.GithubOAuth2',

)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'github.pipeline.enterprise_details',
    'osw.pipeline.two_factor_audit',
    'osw.pipeline.github_details',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'core.pipeline.sync',
)

SOCIAL_AUTH_GITHUB_ENTERPRISE_KEY = get_secret('SOCIAL_AUTH_GITHUB_ENTERPRISE_KEY')
SOCIAL_AUTH_GITHUB_ENTERPRISE_SECRET = get_secret('SOCIAL_AUTH_GITHUB_ENTERPRISE_SECRET')
SOCIAL_AUTH_GITHUB_ENTERPRISE_SCOPE = ['user', 'repo', 'admin:repo_hook', 'admin:org', 'write:public_key']
SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST = get_secret('SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST')
SOCIAL_AUTH_GITHUB_ENTERPRISE_USER_FIELDS = ('first_name', 'last_name', 'username', 'email', 'contractor',)
SOCIAL_AUTH_GITHUB_KEY = get_secret('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = get_secret('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['user', 'repo', 'admin:repo_hook', 'write:org', 'write:public_key']

# ids of all orgs belonging to the entity
GH_ORG_IDS = get_secret('GH_ORG_IDS', (1071563,))

# org for auditing user's 2 factor auth prior to admission into primary org.
GH_2FA_AUDIT_TEAM = get_secret('GH_2FA_AUDIT_TEAM')

# credintials must have admin:org priviliges for the GH_2FA_AUDIT_ORG
GH_2FA_ADMIN_CREDENTIALS = get_secret('GH_2FA_ADMIN_CREDENTIALS') # A requests.auth.HTTPBasicAuth object

# READ ONLY CREDENTIALS
GH_ADMIN_CREDENTIALS = get_secret('GH_ADMIN_CREDENTIALS') # A requests.auth.HTTPBasicAuth object

# READ ONLY CREDENTIALS
GHE_ADMIN_CREDENTIALS = get_secret('GHE_ADMIN_CREDENTIALS') # A requests.auth.HTTPBasicAuth object


# Application definition

INSTALLED_APPS = (
    'tiles',
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'github',
    'osw',
    'jenkins',
)

HOME_TILES = ('github.ghe_repos', 'github.gh_repos',)
SYNC = ('github',)


GH_TILES = ('osw.join_org',)
GHE_TILES = tuple()
GH_REPO_ACTIONS = tuple()
GHE_REPO_ACTIONS = ('osw.openSource', 'jenkins.createJob')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'devops.urls'

WSGI_APPLICATION = 'devops.wsgi.application'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend', 'dest', 'static'),
)
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'