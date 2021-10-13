from polaris.models import Asset, Transaction
from rest_framework.request import Request
from stellar_sdk.keypair import Keypair

from .mocks import constants


def test_get_distribution_account(mocker, make_wyre_integration, make_wyre_xlm_address):
    stellar_account_address, user_id = make_wyre_xlm_address.split(":")

    wyre = mocker.patch(
        "polaris_wyre.wyre.Wyre.get_account",
        return_value=(stellar_account_address, user_id),
    )
    asset = mocker.Mock(spec=Asset)

    wyre_integration = make_wyre_integration()

    distribution_account = wyre_integration.get_distribution_account(asset)

    wyre.assert_called_once()
    assert distribution_account == stellar_account_address


def test_save_receiving_account_and_memo(
    db, mocker, make_wyre_integration, make_wyre_xlm_address
):
    stellar_account_address, user_id = make_wyre_xlm_address.split(":")

    wyre = mocker.patch(
        "polaris_wyre.wyre.Wyre.get_account",
        return_value=(stellar_account_address, user_id),
    )

    request = mocker.Mock(spec=Request)
    transaction = mocker.Mock(spec=Transaction)

    wyre_integration = make_wyre_integration()

    wyre_integration.save_receiving_account_and_memo(request, transaction)

    wyre.assert_called_once()

    assert transaction.receiving_anchor_account == stellar_account_address
    assert transaction.memo_type == Transaction.MEMO_TYPES.text
    assert transaction.memo == user_id


def test_submit_deposit_transaction(
    db, mocker, make_wyre_integration, make_transfer_data
):
    destination_address = Keypair.random().public_key
    asset = mocker.Mock(spec=Asset)
    transaction = mocker.Mock(spec=Transaction)

    asset.code = "USDC"
    asset.significant_decimals = 2

    transaction.asset = asset
    transaction.amount_in = 100
    transaction.amount_fee = 3
    transaction.to_address = destination_address

    amount = amount = round(
        transaction.amount_in - transaction.amount_fee,
        asset.significant_decimals,
    )

    transfer_data = make_transfer_data(
        currency=transaction.asset.code,
        amount=amount,
        destination=f"stellar:{transaction.to_address}",
    )

    transfer_id = "TF_GDQ844E2EZG"

    wyre_create_transfer_mock = mocker.patch(
        "polaris_wyre.wyre.Wyre.create_transfer",
        return_value=transfer_id,
    )
    wyre_get_stellar_transaction_id_mock = mocker.patch(
        "polaris_wyre.wyre.Wyre.get_stellar_transaction_id",
        return_value="fcbe60c421785be718ba422ef5e6883f58284ec058b7017e5f7886e33330e549",
    )
    mocker.patch(
        "stellar_sdk.call_builder.transactions_call_builder.TransactionsCallBuilder.call",
        return_value=constants.STELLAR_TRANSACTION_SUCCESS_RESPONSE,
    )

    wyre_integration = make_wyre_integration()
    transaction_info = wyre_integration.submit_deposit_transaction(transaction)

    wyre_create_transfer_mock.assert_called_once_with(transfer_data)
    wyre_get_stellar_transaction_id_mock.assert_called_once_with(transfer_id)

    assert transaction_info == constants.STELLAR_TRANSACTION_SUCCESS_RESPONSE
