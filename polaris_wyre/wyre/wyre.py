from typing import Tuple

from polaris_wyre.wyre.dtos import TransferData
from .api import TEST_BASE_URL, WyreAPI

COMPLETED_STATUS = "COMPLETED"
FAILED_STATUS = "FAILED"


class Wyre:
    def __init__(
        self, api_token: str = "", account_id: str = "", api_url: str = TEST_BASE_URL
    ):
        self.wyre_api = WyreAPI(
            api_token=api_token, account_id=account_id, api_url=api_url
        )

    def get_account(self) -> Tuple[str, str]:
        """
        Gets the Stellar's account address from the Wyre's account information.

        :return: Returns a tuple containing the account data and the user id.
        """
        response_data = self.wyre_api.get_account()
        return response_data["depositAddresses"]["XLM"].split(":")

    def get_stellar_transaction_id(self, transfer_id: str) -> str:
        """
        Gets the Stellar Network's transaction id.

        :param: The Wyre's transfer id.
        :return: Returns a string containing the Stellar Network transaction id.
        """
        while True:
            response_data = self.wyre_api.get_transfer_by_id(transfer_id)
            if response_data["status"] == FAILED_STATUS:
                # TODO: improve RuntimeError message with a better description
                raise RuntimeError("Wyre failed to complete the transfer.")
            if response_data["status"] == COMPLETED_STATUS:
                break
        return response_data["blockchainTx"]["networkTxId"]

    def create_transfer(self, transfer_data: TransferData) -> str:
        """
        Builds a transfer based on the given transfer data.

        :param: A :class:`TransferData` instance containing the transfer
        information.
        :return: Returns Wyre's transfer id.
        """
        response_data = self.wyre_api.create_transfer(transfer_data)
        return response_data["id"]
