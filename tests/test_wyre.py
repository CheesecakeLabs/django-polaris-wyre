from decimal import Decimal

import pytest
from django.conf import settings
from stellar_sdk.keypair import Keypair

from polaris_wyre.wyre.dtos import TransferData
from .mocks import wyre as wyre_mocks


def test_get_account(mocker, make_wyre, make_wyre_xlm_address):
    stellar_address, user_id = make_wyre_xlm_address.split(":")

    wyre_api_mock = mocker.patch(
        "polaris_wyre.wyre.api.WyreAPI.get_account",
        return_value={"depositAddresses": {"XLM": make_wyre_xlm_address}},
    )

    wyre = make_wyre()
    wyre_stellar_address, wyre_user_id = wyre.get_account()

    wyre_api_mock.assert_called_once()

    assert stellar_address == wyre_stellar_address
    assert user_id == wyre_user_id


def test_get_stellar_transaction_id_success(mocker, make_wyre):
    network_tx_id = "7586ec0223fc193da6fc609b92a62a96ae86258873480d8bc288723e29028cd3"

    wyre_api_mock = mocker.patch(
        "polaris_wyre.wyre.api.WyreAPI.get_transfer_by_id",
        side_effect=[
            {"status": "PENDING"},
            {"status": "PENDING"},
            {"status": "PENDING"},
            {"status": "COMPLETED", "blockchainTx": {"networkTxId": network_tx_id}},
        ],
    )

    wyre = make_wyre()
    stellar_transaction_id = wyre.get_stellar_transaction_id("TF_ABC1234")

    wyre_api_mock.assert_called()

    assert stellar_transaction_id == network_tx_id


def test_get_stellar_transaction_id_runtime_error(mocker, make_wyre):
    wyre_api_mock = mocker.patch(
        "polaris_wyre.wyre.api.WyreAPI.get_transfer_by_id",
        side_effect=[
            {"status": "PENDING"},
            {"status": "PENDING"},
            {"status": "PENDING"},
            {"status": "FAILED"},
        ],
    )

    wyre = make_wyre()

    with pytest.raises(RuntimeError, match="Wyre failed to complete the transfer."):
        wyre.get_stellar_transaction_id("TF_ABC1234")

    wyre_api_mock.assert_called()


def test_create_transfer(mocker, make_wyre):
    currency = "USDC"
    amount = Decimal("100")
    destination = Keypair.random().public_key

    transfer_data = TransferData(
        currency=currency, amount=amount, destination=destination
    )

    wyre_api_mock = mocker.patch(
        "polaris_wyre.wyre.api.WyreAPI.create_transfer",
        return_value=wyre_mocks.create_transfer_data(
            account_id=settings.WYRE_ACCOUNT_ID,
            currency=transfer_data.currency,
            amount=transfer_data.amount,
            destination=transfer_data.destination,
        ),
    )

    wyre = make_wyre()
    response_data = wyre.create_transfer(transfer_data)

    wyre_api_mock.assert_called_with(transfer_data)

    assert response_data == wyre_api_mock.return_value
