import django
from stellar_sdk import Keypair


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        SECRET_KEY="not very secret in tests",
        MIDDLEWARE=(
            "django.middleware.common.CommonMiddleware",
            "corsheaders.middleware.CorsMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "polaris",
        ),
    )

    # Polaris settings
    settings.POLARIS_ACTIVE_SEPS = ["sep-1", "sep-10", "sep-24"]
    settings.POLARIS_SIGNING_SEED = Keypair.random().secret
    settings.POLARIS_SERVER_JWT_KEY = "notsosecretkey"
    settings.POLARIS_HOST_URL = "https://example.com/"
    settings.SESSION_COOKIE_SECURE = True

    django.setup()
