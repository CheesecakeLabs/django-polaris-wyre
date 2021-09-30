# Django Polaris Wyre

Django Polaris Wyre custodial solution is a Django app that aims to extend the [Django Polaris](https://github.com/stellar/django-polaris) standard functionalities, allowing for the custody of the anchor distribution account to be held by [Wyre](https://www.sendwyre.com/) as a secure partner.

## Dependencies

- django-polaris > 2.0
- requests < 3, >= 2.0

## Installation

```shell
$ pip install django-polaris-wyre
```

```python
# settings.py

INSTALLED_APPS = [
    ...
    # polaris dependencies
    "rest_framework",
    "corsheaders",
    "polaris",
    # polaris wyre dependency
    "polaris_wyre",
    ...
]
```
## How to use

To use the Wyre's wallet, it is necessary to import `WyreIntegration` class from `polaris_wyre.wyre.integration` package and pass an instance of it as the `custody` parameter in the Polaris' `register_integrations` function.

```py
# apps.py

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "my_app"

    def ready(self):
        from polaris.integrations import register_integrations
        from polaris_wyre.wyre.integration import WyreIntegration
        from .integrations import (
            ...
            MyRailsIntegration,
        )

        register_integrations(
            ...,
            rails=MyRailsIntegration(),
            custody=WyreIntegration(
                api_url="https://api.sendwyre.com",
                api_token="myapikey",
                account_id="myaccountid",
            ),
        )
```

The `WyreIntegration` class has the following parameters:

- **api_url**: The Wyre's API base URL. Use `https://api.sendwyre.com` for the production environment and `https://api.testwyre.com` for the test environment.

- **api_token**: The API Token for the Wyre account. It can be generated on your Wyre account by navigating to "Your Account" -> "API Keys". Here, click on the "Add API Key" button to add a token. On the following screen, fill in the information about the token that will be created and click on "Save" button. After this you should receive an "API Key" and "Secret Key", you'll use the "Secret Key" as the API Token.

- **account_id**: Your Wyre account id. You can find it by navigating to "Your Account" -> "Basic Info". Here, look above of your profile picture and you should see your `account_id`.

After this you are ready to go.
