from requests.exceptions import HTTPError


class WyreAPIError(HTTPError):
    pass
