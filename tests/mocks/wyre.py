from decimal import Decimal

import requests
from rest_framework import status


def get_account_data(*, account_id: str = "") -> dict:
    return {
        "id": f"{account_id}",
        "createdAt": 1630431947000,
        "updatedAt": 1631279485000,
        "referralUrl": None,
        "apnsToken": None,
        "status": "APPROVED",
        "stripeAccountId": None,
        "profile": {
            "firstName": "John",
            "lastName": "Doe",
            "language": "en",
            "address": {
                "street1": "Wolf Street",
                "street2": None,
                "city": "New York",
                "state": "NY",
                "postalCode": "12345",
                "country": "US",
            },
            "businessAccount": True,
            "taxId": None,
            "doingBusinessAs": None,
            "website": None,
            "partnerLink": None,
            "ssn": None,
            "dateOfBirth": 1619308800000,
            "notifyEmail": True,
            "notifyCellphone": True,
            "notifyApnsDevice": None,
            "onboardingDashboardCompleted": False,
            "displayCurrency": "USD",
            "cpfNumber": None,
            "type": "BUSINESS",
            "vertical": "BUSINESS",
            "ethereumVerificationAddress": None,
            "companyTitle": "Software Engineer",
            "partnerDisplayName": None,
            "companyName": "Stellar",
            "companyRegistrationNumber": None,
            "occupation": None,
            "purposeOfAccount": None,
            "country": "US",
            "name": "John Doe",
        },
        "paymentMethods": [
            {
                "id": "PA_XFC77WCA4RU",
                "owner": f"account:{account_id}",
                "createdAt": 1631279477000,
                "name": "Plaid Checking 0000",
                "defaultCurrency": "USD",
                "fingerprint": None,
                "status": "ACTIVE",
                "statusMessage": None,
                "waitingPrompts": [],
                "linkType": "LOCAL_TRANSFER",
                "beneficiaryType": "UNKNOWN",
                "supportsDeposit": True,
                "nameOnMethod": None,
                "last4Digits": "0000",
                "brand": None,
                "expirationDisplay": None,
                "countryCode": "US",
                "nickname": "john_doe",
                "rejectionMessage": None,
                "disabled": False,
                "supportsPayment": True,
                "chargeableCurrencies": ["USD"],
                "depositableCurrencies": ["USD"],
                "chargeFeeSchedule": None,
                "depositFeeSchedule": None,
                "minCharge": None,
                "maxCharge": None,
                "minDeposit": None,
                "maxDeposit": None,
                "documents": [],
                "blockchains": {},
                "liquidationBalances": {},
                "srn": "paymentmethod:PA_XFC77WCA4RU",
            }
        ],
        "identities": [
            {
                "namespace": None,
                "srn": "cellphone:+9999999999999",
                "createdAt": 1630432203000,
                "verifiedAt": 1631279362000,
                "verified": True,
            },
            {
                "namespace": None,
                "srn": "email:johndoe@wyre.com",
                "createdAt": 1630431947000,
                "verifiedAt": 1630432152000,
                "verified": True,
            },
        ],
        "depositAddresses": {
            "BTC": "mvzuBXUHaPKQ9KnasppNYkbc867VG6AHRa",
            "XLM": "GD7WXI7AOAK2CIPZVBEFYLS2NQZI2J4WN4HFYQQ4A2OMFVWGWAL3IW7K:DGXMTLDFRBE",
            "AVAX": "X-fuji1nzajamnydckvn6jdg0jd49v4yeerqganrwq6e6",
            "ETH": "0x7ec9cd67cf159926601fdf08df3521895962c352",
        },
        "ledgers": [
            {
                "srn": f"account:{account_id}",
                "currency": "BTC",
                "balance": 0.00249625000000000000,
                "pendingBalance": 0e-20,
                "minimumBalance": 0e-20,
                "totalBalance": 0.00249625000000000000,
            },
            {
                "srn": f"account:{account_id}",
                "currency": "USD",
                "balance": 21.94000000000000000000,
                "pendingBalance": 100.00000000000000000000,
                "minimumBalance": 0e-20,
                "totalBalance": 121.94000000000000000000,
            },
            {
                "srn": f"account:{account_id}",
                "currency": "USDC",
                "balance": 31.70287800000000000000,
                "pendingBalance": 0e-20,
                "minimumBalance": 0e-20,
                "totalBalance": 31.70287800000000000000,
            },
            {
                "srn": f"account:{account_id}",
                "currency": "XLM",
                "balance": 25.12932951451477214600,
                "pendingBalance": 0e-20,
                "minimumBalance": 0e-20,
                "totalBalance": 25.12932951451477214600,
            },
        ],
        "session": {
            "id": "UQWA3TDCXUU",
            "owner": f"account:{account_id}",
            "createdAt": 1631707751000,
            "seenAt": 1631713025000,
            "expiresAt": 1631714825000,
            "deviceType": None,
            "apiSession": False,
            "ipAddress": "127.0.0.1",
            "language": "en",
            "mfaRequired": False,
            "mfaAuthedAt": None,
            "mfaTokenDispatchedAt": None,
            "ipLock": False,
            "lockedIpAddresses": [],
            "destSrnWhitelist": [],
            "readonly": False,
            "mfaAuthorized": False,
            "city": None,
            "country": None,
        },
        "documents": [],
        "srnLimits": [],
        "email": "johndoe@wyre.com",
        "pusherChannel": "ba24a5a417fa0a8425b4fcd01016f21b",
        "srn": f"account:{account_id}",
        "verified": True,
        "cellphone": "+9999999999999",
        "totalBalances": {
            "BTC": 0.00249625000000000000,
            "XLM": 25.12932951451477214600,
            "USDC": 31.70287800000000000000,
            "USD": 121.94000000000000000000,
        },
        "availableBalances": {
            "BTC": 0.00249625000000000000,
            "XLM": 25.12932951451477214600,
            "USDC": 31.70287800000000000000,
            "USD": 21.94000000000000000000,
        },
        "loc": {},
        "emailIdentity": {
            "namespace": None,
            "srn": "email:johndoe@wyre.com",
            "createdAt": 1630431947000,
            "verifiedAt": 1630432152000,
            "verified": True,
        },
        "loginAt": 1631707751000,
        "lastLoginIp": "127.0.0.1",
        "lastLoginLocation": None,
        "type": "BUSINESS",
    }


def get_account_response(
    *,
    account_id: str = "",
    status_code: int = status.HTTP_200_OK,
    reason: str = "",
    url: str = "",
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.reason = reason
    response.url = url
    response.json = lambda: get_account_data(account_id=account_id)

    return response


def get_transfer_by_id_data(*, account_id: str = "", transfer_id: str = "") -> dict:
    # TODO: improve payload with a better example
    return {
        "exchangeRate": None,
        "createdAt": 1631726348000,
        "sourceAmount": 5.01001,
        "destCurrency": "XLM",
        "sourceCurrency": "XLM",
        "destAmount": 5,
        "dest": "stellar:GB4S2NHN7DIQVDTZY3QIUNDFV5LZNOO6FS5PO2NOCQ3MBJCVUIBFTJH3",
        "fees": {"XLM": 0.010010000000000000},
        "totalFees": 0.01001,
        "customId": None,
        "completedAt": None,
        "cancelledAt": None,
        "failureReason": None,
        "blockchainTx": {
            "id": "TR_84C9RJPHHJB",
            "networkTxId": "7586ec0223fc193da6fc609b92a62a96ae86258873480d8bc288723e29028cd3",
            "blockTime": None,
            "blockhash": None,
            "amount": 5,
            "address": "GB4S2NHN7DIQVDTZY3QIUNDFV5LZNOO6FS5PO2NOCQ3MBJCVUIBFTJH3",
            "memo": "",
        },
        "expiresAt": 1631727248000,
        "updatedAt": None,
        "reversalReason": None,
        "reversingSubStatus": None,
        "pendingSubStatus": "IN_REVIEW",
        "estimatedArrival": 1632344153592,
        "statusHistories": [
            {
                "id": "C79LWE3WLWU",
                "transferId": transfer_id,
                "createdAt": 1631726349000,
                "type": "OUTGOING",
                "statusOrder": 0,
                "statusDetail": "Initiating Transfer",
                "state": "INITIATED",
                "failedState": None,
            },
            {
                "id": "ZPQM3CWH2A8",
                "transferId": transfer_id,
                "createdAt": 1631726349000,
                "type": "OUTGOING",
                "statusOrder": 400,
                "statusDetail": "Processing Deposit",
                "state": "PENDING",
                "failedState": None,
            },
        ],
        "message": None,
        "id": transfer_id,
        "owner": f"account:{account_id}",
        "source": f"account:{account_id}",
        "status": "COMPLETED",
    }


def get_transfer_by_id_response(
    *,
    account_id: str = "",
    transfer_id: str = "",
    status_code: int = status.HTTP_200_OK,
    reason: str = "",
    url: str = "",
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.reason = reason
    response.url = url
    response.json = lambda: get_transfer_by_id_data(
        account_id=account_id, transfer_id=transfer_id
    )

    return response


def create_transfer_data(
    *,
    account_id: str = "",
    currency: str = "",
    amount: Decimal = Decimal(),
    destination: str = "",
) -> dict:
    return {
        "exchangeRate": None,
        "createdAt": 1631815455000,
        "sourceAmount": amount + Decimal("0.02001"),
        "destCurrency": currency,
        "sourceCurrency": currency,
        "destAmount": amount,
        "dest": destination,
        "fees": {currency: 0.020010000000000000},
        "totalFees": 0.020010000000000000,
        "customId": None,
        "completedAt": None,
        "cancelledAt": None,
        "failureReason": None,
        "blockchainTx": None,
        "expiresAt": 1631816355000,
        "updatedAt": None,
        "reversalReason": None,
        "reversingSubStatus": None,
        "pendingSubStatus": "IN_REVIEW",
        "estimatedArrival": 1632420255310,
        "statusHistories": [],
        "message": None,
        "id": "TF_GDQ844E2EZG",
        "owner": f"account:{account_id}",
        "source": f"account:{account_id}",
        "status": "PENDING",
    }


def create_transfer_response(
    *,
    account_id: str = "",
    currency: str = "",
    amount: Decimal = Decimal(),
    destination: str = "",
    status_code: int = status.HTTP_200_OK,
    reason: str = "",
    url: str = "",
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.reason = reason
    response.url = url
    response.json = lambda: create_transfer_data(
        account_id=account_id,
        currency=currency,
        amount=amount,
        destination=destination,
    )

    return response
