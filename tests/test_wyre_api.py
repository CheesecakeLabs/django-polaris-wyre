from urllib.parse import urljoin

import pytest
from django.conf import settings
from rest_framework import status

from polaris_wyre.helpers.exceptions import WyreAPIError
from polaris_wyre.wyre.api import TEST_BASE_URL
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
    response = wyre_api.get_account()

    wyre_request_mock.assert_called_once_with(
        urljoin(wyre_api.API_URL, "v2/account"),
    )

    assert response == wyre_request_mock.return_value.json()
    assert settings.WYRE_ACCOUNT_ID == response["id"]


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
    response = wyre_api.get_transfer_by_id(transfer_id=transfer_id)

    wyre_request_mock.assert_called_once_with(
        urljoin(wyre_api.API_URL, f"v3/transfers/{transfer_id}"),
    )

    assert response == wyre_request_mock.return_value.json()
    assert f"account:{settings.WYRE_ACCOUNT_ID}" == response["source"]
    assert response["id"] == transfer_id


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


def test_create_transfer_success(mocker, make_wyre_api, make_transfer_data):
    transfer_data = make_transfer_data()

    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_POST_MOCK,
        return_value=wyre_mocks.create_transfer_response(
            account_id=settings.WYRE_ACCOUNT_ID,
            currency=transfer_data.currency,
            amount=transfer_data.amount,
            destination=transfer_data.destination,
        ),
    )

    data = {
        "autoConfirm": True,
        "source": f"account:{settings.WYRE_ACCOUNT_ID}",
        "sourceCurrency": transfer_data.currency,
        "sourceAmount": str(transfer_data.amount),
        "dest": transfer_data.destination,
        "destCurrency": transfer_data.currency,
    }

    wyre_api = make_wyre_api()
    response = wyre_api.create_transfer(transfer_data)

    wyre_request_mock.assert_called_once_with(
        urljoin(wyre_api.API_URL, f"v3/transfers"), json=data
    )

    assert response == wyre_request_mock.return_value.json()
    assert response["source"] == f"account:{settings.WYRE_ACCOUNT_ID}"
    assert response["destAmount"] == transfer_data.amount
    assert response["dest"] == transfer_data.destination
    assert (
        response["destCurrency"] == transfer_data.currency == response["sourceCurrency"]
    )


def test_create_transfer_bad_request(mocker, make_wyre_api, make_transfer_data):
    transfer_data = make_transfer_data()

    data = {
        "autoConfirm": True,
        "source": f"account:{settings.WYRE_ACCOUNT_ID}",
        "sourceCurrency": transfer_data.currency,
        "sourceAmount": str(transfer_data.amount),
        "dest": transfer_data.destination,
        "destCurrency": transfer_data.currency,
    }

    url = urljoin(TEST_BASE_URL, "v3/transfers")
    wyre_request_mock = mocker.patch(
        REQUEST_METHOD_POST_MOCK,
        return_value=wyre_mocks.create_transfer_response(
            account_id=settings.WYRE_ACCOUNT_ID,
            currency=transfer_data.currency,
            amount=transfer_data.amount,
            destination=transfer_data.destination,
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
