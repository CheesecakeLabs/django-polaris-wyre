from urllib.parse import urljoin

import requests

from polaris_wyre.helpers.exceptions import WyreAPIError
from .dtos import TransferData

TEST_BASE_URL = "https://api.testwyre.com"


# TODO: add methods description
class WyreAPI:
    def __init__(
        self,
        api_token: str = "",
        account_id: str = "",
        api_url: str = TEST_BASE_URL,
    ):
        self.API_TOKEN = api_token
        self.ACCOUNT_ID = account_id
        self.API_URL = api_url

        base_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.API_TOKEN}",
        }

        self.session = requests.Session()
        self.session.headers.update(**base_headers)

    @staticmethod
    def _handle_response(response: requests.Response) -> dict:
        """
        Handle the Wyre's API response. In case the response is not
        successful, it raises a :class:`WyreAPIError`, otherwise it
        returns the response's JSON.

        :return: Returns Wyre's API response's JSON.
        """
        if response.ok:
            return response.json()
        msg = f"{response.status_code} Error: {response.reason} for url {response.url}. Response Text: {response.text}"
        raise WyreAPIError(msg, response=response)

    def get_account(self) -> dict:
        url = urljoin(self.API_URL, "v2/account")
        response = self.session.get(url)
        return self._handle_response(response)

    def get_transfer_by_id(self, transfer_id: str) -> dict:
        url = urljoin(self.API_URL, f"v3/transfers/{transfer_id}")
        response = self.session.get(url)
        return self._handle_response(response)

    def create_transfer(self, transfer_data: TransferData) -> dict:
        url = urljoin(self.API_URL, "v3/transfers")
        data = {
            "autoConfirm": True,
            "source": f"account:{self.ACCOUNT_ID}",
            "sourceCurrency": transfer_data.currency,
            "sourceAmount": str(transfer_data.amount),
            "dest": transfer_data.destination,
            "destCurrency": transfer_data.currency,
        }

        response = self.session.post(url, json=data)

        return self._handle_response(response)
