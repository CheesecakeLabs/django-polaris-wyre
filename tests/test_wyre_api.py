from decimal import Decimal
from urllib.parse import urljoin

import pytest
from django.conf import settings
from rest_framework import status
from stellar_sdk import Keypair

from polaris_wyre.helpers.exceptions import WyreAPIError
from polaris_wyre.wyre.api import TEST_BASE_URL
from polaris_wyre.wyre.dtos import TransferData
from .mocks import wyre as wyre_mocks


REQUEST_METHOD_GET_MOCK = "requests.Session.get"
REQUEST_METHOD_POST_MOCK = "requests.Session.post"


def test_get_account_success(mocker, make_wyre_api):
    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_GET_MOCK,
        return_value=wyre_mocks.get_account_response(
            account_id=settings.WYRE_ACCOUNT_ID
        ),
    )

    wyre_api = make_wyre_api()
    response_data = wyre_api.get_account()

    wyre_request_mock.assert_called_once_with(
        urljoin(wyre_api.API_URL, "v2/account"),
    )

    assert response_data == wyre_request_mock.return_value.json()
    assert settings.WYRE_ACCOUNT_ID == response_data["id"]


def test_get_account_unauthorized(mocker, make_wyre_api):
    url = urljoin(TEST_BASE_URL, "v2/account")

    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_GET_MOCK,
        return_value=wyre_mocks.get_account_response(
            account_id=settings.WYRE_ACCOUNT_ID,
            status_code=status.HTTP_401_UNAUTHORIZED,
            url=url,
            reason="Unauthorized",
        ),
    )

    wyre_api = make_wyre_api()

    with pytest.raises(
        WyreAPIError,
        match=f"401 Error: Unauthorized for url {url}. Response Text: ",
    ):
        wyre_api.get_account()

    wyre_request_mock.assert_called_once_with(url)


def test_get_transfer_by_id_success(mocker, make_wyre_api):
    transfer_id = "TF_WXP3YR7JJW8"
    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_GET_MOCK,
        return_value=wyre_mocks.get_transfer_by_id_response(
            account_id=settings.WYRE_ACCOUNT_ID, transfer_id=transfer_id
        ),
    )

    wyre_api = make_wyre_api()
    response_data = wyre_api.get_transfer_by_id(transfer_id=transfer_id)

    wyre_request_mock.assert_called_once_with(
        urljoin(wyre_api.API_URL, f"v3/transfers/{transfer_id}"),
    )

    assert response_data == wyre_request_mock.return_value.json()
    assert f"account:{settings.WYRE_ACCOUNT_ID}" == response_data["source"]
    assert response_data["id"] == transfer_id


def test_get_transfer_by_id_unauthorized(mocker, make_wyre_api):
    transfer_id = "TF_WXP3YR7JJW8"
    url = urljoin(TEST_BASE_URL, f"v3/transfers/{transfer_id}")

    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_GET_MOCK,
        return_value=wyre_mocks.get_transfer_by_id_response(
            account_id=settings.WYRE_ACCOUNT_ID,
            transfer_id=transfer_id,
            status_code=status.HTTP_401_UNAUTHORIZED,
            url=url,
            reason="Unauthorized",
        ),
    )

    wyre_api = make_wyre_api()

    with pytest.raises(
        WyreAPIError,
        match="401 Error: Unauthorized for url https://api.testwyre.com/v3/transfers/TF_WXP3YR7JJW8. Response Text: ",
    ):
        wyre_api.get_transfer_by_id(transfer_id=transfer_id)

    wyre_request_mock.assert_called_once_with(url)


def test_create_transfer_success(mocker, make_wyre_api):
    currency = "USDC"
    amount = Decimal("10")
    destination = f"stellar:{Keypair.random().public_key}"

    transfer_data = TransferData.create_transfer_data(
        currency=currency,
        amount=amount,
        destination=destination,
    )

    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_POST_MOCK,
        return_value=wyre_mocks.create_transfer_response(
            account_id=settings.WYRE_ACCOUNT_ID,
            currency=currency,
            amount=amount,
            destination=destination,
        ),
    )

    data = {
        "autoConfirm": True,
        "source": f"account:{settings.WYRE_ACCOUNT_ID}",
        "sourceCurrency": currency,
        "sourceAmount": str(amount),
        "dest": destination,
        "destCurrency": currency,
    }

    wyre_api = make_wyre_api()
    response_data = wyre_api.create_transfer(transfer_data)

    wyre_request_mock.assert_called_once_with(
        urljoin(wyre_api.API_URL, f"v3/transfers"), json=data
    )

    assert response_data == wyre_request_mock.return_value.json()
    assert response_data["source"] == f"account:{settings.WYRE_ACCOUNT_ID}"
    assert response_data["destAmount"] == amount
    assert response_data["dest"] == destination
    assert response_data["destCurrency"] == currency == response_data["sourceCurrency"]


def test_create_transfer_bad_request(mocker, make_wyre_api):
    currency = "USDC"
    amount = Decimal("10")
    destination = f"stellar:{Keypair.random().public_key}"

    transfer_data = TransferData.create_transfer_data(
        currency=currency,
        amount=amount,
        destination=destination,
    )

    data = {
        "autoConfirm": True,
        "source": f"account:{settings.WYRE_ACCOUNT_ID}",
        "sourceCurrency": currency,
        "sourceAmount": str(amount),
        "dest": destination,
        "destCurrency": currency,
    }

    url = urljoin(TEST_BASE_URL, "v3/transfers")
    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_POST_MOCK,
        return_value=wyre_mocks.create_transfer_response(
            account_id=settings.WYRE_ACCOUNT_ID,
            currency=currency,
            amount=amount,
            destination=destination,
            status_code=status.HTTP_400_BAD_REQUEST,
            url=url,
            reason="Bad Request",
        ),
    )

    wyre_api = make_wyre_api()
    with pytest.raises(
        WyreAPIError,
        match="400 Error: Bad Request for url https://api.testwyre.com/v3/transfers. Response Text: ",
    ):
        wyre_api.create_transfer(transfer_data)

    wyre_request_mock.assert_called_once_with(url, json=data)
