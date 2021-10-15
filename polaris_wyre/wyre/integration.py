from polaris import settings as polaris_settings
from polaris.models import Asset, Transaction
from polaris.integrations import CustodyIntegration
from polaris_wyre.wyre.dtos import TransferData
from rest_framework.request import Request
from stellar_sdk.server import Server

from . import Wyre
from .api import TEST_BASE_URL


class WyreIntegration(CustodyIntegration):
    def __init__(
        self, api_token: str = "", account_id: str = "", api_url: str = TEST_BASE_URL
    ):
        self.wyre = Wyre(api_token=api_token, account_id=account_id, api_url=api_url)

    def get_distribution_account(self, asset: Asset) -> str:
        """
        Return the Stellar account used to receive payments of `asset`. This
        method is a replacement for the ``Asset.distribution_account`` property
        which is derived from the ``Asset.distribution_seed`` database column.
        This means that the same distribution account should always be returned
        for the same asset. **Do not implement this method if your custody service
        provider does not support using the same Stellar account for all incoming
        payments of an asset.** Some custody service providers provide a Stellar
        account and memo to use as the destination of an incoming payment on a
        per-transaction basis, with no guaranteed consistency for the Stellar
        account provided.
        The ``watch_transactions`` command assumes this method is implemented.
        If this method is not implemented, another approach to detecting and
        matching incoming payments must be used.
        :param asset: the asset sent in payments to the returned Stellar account
        """
        stellar_account_address, _ = self.wyre.get_account()
        return stellar_account_address

    def save_receiving_account_and_memo(
        self, request: Request, transaction: Transaction
    ) -> None:
        """
        Save the Stellar account that the client should use as the destination
        of the payment transaction to ``Transaction.receiving_anchor_account``,
        the string representation of the memo the client should attach to the
        transaction to ``Transaction.memo``, and the type of that memo to
        ``Transaction.memo_type``.
        This method is only called once for a given transaction. The values
        saved will be returned to the client in the response to this request or
        in future ``GET /transaction`` responses.
        **Polaris assumes ``Transaction.save()`` is called within this method.**
        The memo saved to the transaction object _must_ be unique to the
        transaction, since the anchor is expected to match the database record
        represented by `transaction` with the on-chain transaction submitted.
        This function differs from ``get_distribution_account()`` by allowing the
        anchor to return any Stellar account that can be used to receive a payment.
        This is ideal when the account used is determined by a custody service
        provider that does not guarantee that the account provided will be the
        account provided for future transactions.
        :param request: the request that initiated the call to this function
        :param transaction: the transaction a Stellar account and memo must be
            saved to
        """
        stellar_account_address, user_id = self.wyre.get_account()
        transaction.receiving_anchor_account = stellar_account_address
        # TODO: Find a way to let the memo unique when integrating with Wyre
        transaction.memo_type = Transaction.MEMO_TYPES.text
        transaction.memo = user_id
        transaction.save()

    def submit_deposit_transaction(
        self, transaction: Transaction, has_trustline: bool = True
    ) -> dict:
        """
        Submit the transaction to the Stellar network using the anchor's custody
        service provider and return the JSON body of the associated
        ``GET /transaction/:id`` Horizon response.
        If ``self.claimable_balances_supported`` is ``True``, Polaris may call
        this method when the destination account does not yet have a trustline
        to ``Transaction.asset``. In this case, the anchor should send the
        deposit as a claimable balance instead of a payment or path payment. Use
        the `has_trustline` parameter to determine which operations to use.
        If ``self.claimable_balances_supported`` is ``False``, this method will only
        be called when the destination account exists and has a trustline to
        ``Transaction.asset``.
        :param transaction: the ``Transaction`` object representing the Stellar
            transaction that should be submitted to the network
        :param has_trustline: whether or not the destination account has a trustline
            for the requested asset
        """
        amount = round(
            transaction.amount_in - transaction.amount_fee,
            transaction.asset.significant_decimals,
        )
        transfer_data = TransferData(
            currency=transaction.asset.code,
            amount=amount,
            destination=f"stellar:{transaction.to_address}",
        )

        transfer_id = self.wyre.create_transfer(transfer_data)
        transaction_id = self.wyre.get_stellar_transaction_id(transfer_id)

        with Server(horizon_url=polaris_settings.HORIZON_URI) as server:
            return server.transactions().transaction(transaction_id).call()

    def create_destination_account(self, transaction: Transaction) -> dict:
        """
        Wyre doesn't support account creation.
        """
        raise NotImplementedError()

    def requires_third_party_signatures(self, transaction: Transaction) -> bool:
        """
        Return ``True`` if the transaction requires signatures neither the anchor
        nor custody service can provide as a direct result of Polaris calling
        ``submit_deposit_transaction()``, ``False`` otherwise.
        If ``True`` is returned, Polaris will save a transaction envelope to
        ``Transaction.envelope_xdr`` and set ``Transaction.pending_signatures`` to
        ``True``. The anchor will then be expected to collect the signatures required,
        updating ``Transaction.envelope_xdr``, and resetting
        ``Transaction.pending_signatures`` back to ``False``. Finally, Polaris will
        detect this change in state and pass the transaction to
        ``submit_deposit_transaction()``.
        Note that if third party signatures are required, Polaris expects the anchor
        to provide a channel account to be used as the transaction source account.
        See the :ref:`anchoring-multisignature-assets` documentation for more
        information.
        """
        return False

    @property
    def claimable_balances_supported(self) -> bool:
        """
        Return ``True`` if the custody service provider supports sending deposit
        payments in the form of claimable balances, ``False`` otherwise.
        """
        return False

    @property
    def account_creation_supported(self) -> bool:
        """
        Return ``True`` if the custody service provider supports funding Stellar
        accounts not in custody by the provider, ``False`` otherwise.
        """
        return False
