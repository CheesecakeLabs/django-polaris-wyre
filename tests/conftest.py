from typing import Callable

import django
import pytest
from stellar_sdk import Keypair

from polaris_wyre.wyre.api import WyreAPI


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

    # Wyre settigns
    settings.WYRE_API_TOKEN = "myapitoken"
    settings.WYRE_ACCOUNT_ID = "AC_ABCD1234"

    django.setup()


@pytest.fixture
def make_wyre_api() -> Callable:
    from django.conf import settings

    def _make_wyre_api(
        api_token: str = settings.WYRE_API_TOKEN,
        account_id: str = settings.WYRE_ACCOUNT_ID,
    ) -> WyreAPI:
        return WyreAPI(api_token=api_token, account_id=account_id)

    return _make_wyre_api
