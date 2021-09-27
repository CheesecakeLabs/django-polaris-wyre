import secrets
import string
from decimal import Decimal
from typing import Callable

import django
import pytest
from stellar_sdk import Keypair

from polaris_wyre.wyre import Wyre
from polaris_wyre.wyre.api import WyreAPI
from polaris_wyre.wyre.dtos import TransferData

ALPHABET = string.ascii_uppercase + string.digits


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


@pytest.fixture
def make_wyre() -> Callable:
    from django.conf import settings

    def _make_wyre(
        api_token: str = settings.WYRE_API_TOKEN,
        account_id: str = settings.WYRE_ACCOUNT_ID,
    ) -> Wyre:
        return Wyre(api_token=api_token, account_id=account_id)

    return _make_wyre


@pytest.fixture
def make_wyre_xlm_address() -> str:
    stellar_address = Keypair.random().public_key
    user_id = "".join(secrets.choice(ALPHABET) for _ in range(11))
    return f"{stellar_address}:{user_id}"


@pytest.fixture
def make_transfer_data() -> Callable:
    def _make_transfer_data(
        currency: str = "USDC",
        amount: Decimal = Decimal("100"),
        destination: str = f"stellar:{Keypair.random().public_key}",
    ) -> TransferData:
        return TransferData(currency=currency, amount=amount, destination=destination)

    return _make_transfer_data
